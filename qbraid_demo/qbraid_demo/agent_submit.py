"""Submit quoted QPU jobs through the qBraid terminal agent.

The Python process writes OpenQASM and a fixed plan. A `codeq` agent launched
with `qbraid agents launch` then runs `qbraid jobs submit` for each row. The
plan is the whole budget: the agent is told not to add jobs and not to pass
the quoted total.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

from . import circuits

TARGET_SHOTS = {
    "grover": 1000,
    "teleport": 1000,
    "bb84": 500,
    "shor": 256,
    "qaoa": 400,
}
# Larger circuits first so a small device is not preferred just because it is cheap.
EXPERIMENT_ORDER = ("bb84", "shor", "qaoa", "teleport", "grover")


def qbraid_executable() -> str:
    sibling = Path(shutil.which("python3") or "").parent / "qbraid"
    candidates = [Path(__import__("sys").executable).parent / "qbraid", sibling]
    for path in candidates:
        if path.is_file():
            return str(path)
    found = shutil.which("qbraid")
    if found:
        return found
    raise FileNotFoundError("qbraid CLI is not on PATH. Install it with: pip install 'qbraid-cli>=0.12'")


def _route_rank(qrn: str) -> int:
    if qrn.startswith(("aws:", "azure:", "openquantum:")):
        return 2
    return 0


def _dedupe_qpus(qpus):
    best = {}
    for device in qpus:
        key = (device.name, device.numberQubits)
        current = best.get(key)
        if current is None or _route_rank(device.qrn) < _route_rank(current.qrn):
            best[key] = device
    return list(best.values())


def _payload_for(key, device, payloads):
    if key == "bb84":
        full = payloads["bb84"]
        small = payloads["bb84_small"]
        qubits = device.numberQubits or 0
        if qubits >= full["qubits"]:
            return "bb84", full
        if qubits >= small["qubits"]:
            return "bb84_small", small
        return None, None
    payload = payloads[key]
    if (device.numberQubits or 0) < payload["qubits"]:
        return None, None
    return key, payload


def build_hardware_plan(qpus, payloads, quote_fn, fit_shots, ceiling):
    """Fill the credit ceiling with one quoted job per experiment per QPU."""
    qpus = _dedupe_qpus(qpus)
    quotes = []
    for device in qpus:
        for key in EXPERIMENT_ORDER:
            payload_key, payload = _payload_for(key, device, payloads)
            if payload is None:
                continue
            shots = fit_shots(device, TARGET_SHOTS[key])
            quote = quote_fn(device.qrn, shots)
            quote["experiment"] = key
            quote["payload_key"] = payload_key
            quote["role"] = "qpu"
            quote["qubits"] = payload["qubits"]
            quote["device_qubits"] = device.numberQubits
            quote["device_name"] = device.name
            quotes.append(quote)

    remaining = float(ceiling)
    chosen = []
    used = set()

    def take(quote):
        nonlocal remaining
        cost = quote.get("estimated_credits")
        if not quote.get("pricing_available") or cost is None:
            return False
        if cost > remaining + 1e-9:
            return False
        marker = (quote["experiment"], quote["qrn"])
        if marker in used:
            return False
        used.add(marker)
        remaining -= float(cost)
        chosen.append(quote)
        return True

    for key in EXPERIMENT_ORDER:
        pool = [quote for quote in quotes if quote["experiment"] == key]
        pool.sort(key=lambda quote: (quote.get("estimated_credits") is None, quote.get("estimated_credits") or 0, quote["qrn"]))
        for quote in pool:
            if take(quote):
                break

    rest = sorted(
        quotes,
        key=lambda quote: (quote.get("estimated_credits") is None, quote.get("estimated_credits") or 0, quote["qrn"]),
    )
    for quote in rest:
        take(quote)

    return chosen, quotes, remaining


def _write_programs(plan, payloads, programs: Path):
    programs.mkdir(parents=True, exist_ok=True)
    written = {}
    rows = []
    for index, quote in enumerate(plan, start=1):
        payload_key = quote["payload_key"]
        if payload_key not in written:
            qasm = circuits.for_submission(payloads[payload_key]["circuit"])
            path = programs / f"{payload_key}.qasm"
            path.write_text(qasm, encoding="utf-8")
            written[payload_key] = path
        name = f"grid-{quote['experiment']}-{index}"
        rows.append(
            {
                "name": name,
                "experiment": quote["experiment"],
                "payload_key": payload_key,
                "file": str(written[payload_key].relative_to(programs.parent.parent)),
                "device": quote["qrn"],
                "shots": quote["shots"],
                "estimated_credits": quote.get("estimated_credits"),
                "qubits": quote.get("qubits"),
            }
        )
    return rows


def _task_text(rows, ceiling, quoted_total):
    lines = [
        "Submit the qBraid hardware jobs below. Use only `qbraid jobs submit`.",
        f"The quoted total is {quoted_total:.4f} credits. Stop before exceeding {ceiling:.4f} credits.",
        "Do not add devices, shots, or circuits. Do not submit a row twice.",
        "After each command, append one JSON object to results/agent_jobs.jsonl with keys",
        "name, device, experiment, job_id (the jobQrn), and estimated_credits.",
        "When every row has been submitted, print a line that is exactly: AGENT_DONE",
        "",
    ]
    for row in rows:
        tags = json.dumps({"demo": "secure-grid", "experiment": row["experiment"], "hardware": True})
        lines.append(
            "qbraid jobs submit {file} -d {device} -f qasm3 --shots {shots} --name {name} --tags '{tags}' --json".format(
                tags=tags, **row
            )
        )
    return "\n".join(lines) + "\n"


def launch_codeq(cwd: Path, instructions: str, name: str):
    executable = qbraid_executable()
    command = [
        executable,
        "agents",
        "launch",
        "-t",
        "codeq",
        "--backend",
        "tmux",
        "--approval",
        "auto",
        "--detached",
        "--cwd",
        str(cwd),
        "--name",
        name,
        "-i",
        instructions,
    ]
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=120, check=False)
    return {
        "command": " ".join(command[:8]) + " ...",
        "returncode": completed.returncode,
        "stdout": (completed.stdout or "")[-4000:],
        "stderr": (completed.stderr or "")[-4000:],
    }


def _read_agent(name: str, cwd: Path):
    executable = qbraid_executable()
    completed = subprocess.run(
        [executable, "agents", "read", name, "-n", "200"],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    return (completed.stdout or "") + "\n" + (completed.stderr or "")


def _load_jsonl(path: Path):
    records = []
    if not path.exists():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            start, end = line.find("{"), line.rfind("}")
            if start >= 0 and end > start:
                try:
                    records.append(json.loads(line[start : end + 1]))
                except json.JSONDecodeError:
                    continue
    return records


def _job_id(record):
    for key in ("job_id", "jobQrn", "qrn", "id"):
        value = record.get(key)
        if isinstance(value, str) and "qjob" in value:
            return value
    return None


def _match(row, record):
    job_id = _job_id(record)
    if not job_id:
        return False
    device = record.get("device") or record.get("deviceQrn")
    name = record.get("name")
    if name and name == row["name"]:
        return True
    if device and device == row["device"] and record.get("experiment") in (None, row["experiment"]):
        return True
    return False


def collect_agent_submissions(rows, jsonl: Path, agent_name: str, cwd: Path, wait_s: float, step):
    deadline = time.time() + wait_s
    found = {}
    transcript = ""
    while time.time() < deadline:
        transcript = _read_agent(agent_name, cwd)
        for record in _load_jsonl(jsonl):
            for row in rows:
                if row["name"] in found:
                    continue
                if _match(row, record):
                    found[row["name"]] = _job_id(record)
        done = any(line.strip() == "AGENT_DONE" for line in transcript.splitlines())
        if len(found) == len(rows) or (done and found):
            break
        step(f"qBraid agent {agent_name} has submitted {len(found)} of {len(rows)} hardware jobs.")
        time.sleep(8)
    return found, transcript


def submit_with_cli(row, cwd: Path):
    executable = qbraid_executable()
    tags = json.dumps({"demo": "secure-grid", "experiment": row["experiment"], "hardware": True})
    command = [
        executable,
        "jobs",
        "submit",
        row["file"],
        "-d",
        row["device"],
        "-f",
        "qasm3",
        "--shots",
        str(row["shots"]),
        "--name",
        row["name"],
        "--tags",
        tags,
        "--json",
    ]
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=180, check=False)
    text = (completed.stdout or "") + "\n" + (completed.stderr or "")
    job_id = None
    for record in _load_jsonl_text(text):
        job_id = _job_id(record)
        if job_id:
            break
    if completed.returncode != 0 or not job_id:
        raise RuntimeError(text.strip()[-800:] or f"qbraid jobs submit exited {completed.returncode}")
    return job_id


def _load_jsonl_text(text: str):
    records = []
    decoder = json.JSONDecoder()
    index = 0
    while index < len(text):
        start = text.find("{", index)
        if start < 0:
            break
        try:
            record, offset = decoder.raw_decode(text[start:])
        except json.JSONDecodeError:
            index = start + 1
            continue
        if isinstance(record, dict):
            records.append(record)
        index = start + offset
    return records


def jobs_from_ids(provider, rows, job_ids, payloads):
    from qbraid.runtime.native.job import QbraidJob

    pending = []
    notes = []
    for row in rows:
        job_id = job_ids.get(row["name"])
        if not job_id:
            notes.append(f"Not submitted: {row['experiment']} on {row['device']}.")
            continue
        device = provider.get_device(row["device"])
        job = QbraidJob(job_id=job_id, device=device, client=provider.client)
        spec = {
            "experiment": row["experiment"],
            "payload_key": row["payload_key"],
            "qrn": row["device"],
            "shots": row["shots"],
            "noise_model": None,
            "kind": "qpu",
            "qubits": row["qubits"],
            "estimated_credits": row["estimated_credits"],
            "quote_reason": f"quote {row['estimated_credits']} credits",
            "job_id": job_id,
            "status": "SUBMITTED",
            "submitted_by": "qbraid-agent",
        }
        pending.append({"job": job, "spec": spec, "payload": payloads[row["payload_key"]]})
        notes.append(
            f"Submitted {row['experiment']} to {row['device']} ({row['shots']} shots, quote {row['estimated_credits']} credits): {job_id}"
        )
    return pending, notes
