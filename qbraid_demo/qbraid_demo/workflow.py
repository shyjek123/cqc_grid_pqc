"""Agent loop: simulate locally, quote qBraid devices, then submit.

The order matches qBraid's agent instructions. Free simulators go out only when
the quote is 0 credits. A gate-model QPU goes out only when its quote fits under
the credit ceiling and the account balance. Analog devices are skipped; they
cannot run these circuits.
"""

from __future__ import annotations

import csv
import json
import os
import re
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

from . import agent_submit, circuits, figures
from .report import write_report

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"

# Notebook devices that are free at list price. GPU simulators are not on this
# list: they have a daily allowance and then a per-minute price.
FREE_SIMULATORS = (
    "qbraid:qbraid:sim:qir-sv",
    "ionq:ionq:sim:simulator",
    "quantinuum:quantinuum:sim:h2-emulator",
)
NOISE_PREFERENCE = ("aria-1", "forte-1", "aria-2")

GROVER_MARKED = 2
GROVER_N = 4
GROVER8_MARKED = 5
BB84_CLEAN, BB84_EVE = 8, 4
BB84_CLEAN_SMALL, BB84_EVE_SMALL = 4, 2


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _step(trace, message):
    print(message, flush=True)
    trace.append({"utc": _now(), "message": message})


def _pricing(pricing):
    if pricing is None:
        return None
    return {
        "per_task": float(pricing.perTask),
        "per_shot": float(pricing.perShot),
        "per_minute": float(pricing.perMinute),
    }


_SECRET = re.compile(r"qbr_[A-Za-z0-9]+")


def _redact(value):
    if isinstance(value, str):
        return _SECRET.sub("qbr_[redacted]", value)
    if isinstance(value, dict):
        return {str(k): _redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_redact(v) for v in value]
    return value


def _kind(qrn, device_type):
    if device_type == "QPU" or ":qpu:" in qrn:
        return "qpu"
    if "emulator" in qrn:
        return "emulator"
    return "simulator"


def _quote(client, qrn, shots):
    try:
        estimate = client.estimate_cost(qrn, shots)
    except Exception as exc:
        return {
            "qrn": qrn,
            "shots": shots,
            "pricing_available": False,
            "estimated_credits": None,
            "reason": f"{type(exc).__name__}: {exc}",
        }
    cost = None if estimate.estimatedCost is None else float(estimate.estimatedCost)
    return {
        "qrn": qrn,
        "shots": shots,
        "pricing_available": bool(estimate.pricingAvailable),
        "estimated_credits": cost,
        "reason": estimate.reason,
        "pricing_model": estimate.pricingModel,
    }


def _free_ok(qrn, quote, _pricing):
    """Submit an allowlisted simulator only when estimate_cost returns 0 credits."""
    if qrn not in FREE_SIMULATORS:
        return False, "not on the free-simulator list"
    cost = quote.get("estimated_credits")
    if quote.get("pricing_available") and cost == 0:
        return True, "quote is 0 credits"
    if cost is None and quote.get("reason"):
        return False, str(quote["reason"])
    if cost is None:
        return False, "no quote"
    return False, f"quote is {cost:g} credits, above the free-job limit of 0"


def _counts_from(raw, shots):
    values = [float(v) for v in raw.values()]
    if values and max(values) <= 1.0 and abs(sum(values) - 1.0) < 0.05:
        return {str(k).replace(" ", ""): int(round(float(v) * shots)) for k, v in raw.items()}
    return {str(k).replace(" ", ""): int(round(float(v))) for k, v in raw.items()}


def _analyze(kind, counts, payload):
    if not counts:
        return {}
    if kind == "bb84":
        return circuits.analyze_bb84_counts(counts, payload["layout"])
    if kind == "grover":
        return circuits.analyze_grover(counts, payload["marked"], payload["n_items"])
    if kind == "shor":
        return circuits.analyze_shor(counts, payload["n_count"])
    if kind == "teleport":
        return circuits.analyze_teleport(counts)
    if kind == "qaoa":
        return circuits.analyze_qaoa(counts)
    return {}


def run_local(trace):
    _step(trace, "Build the circuits from src/ and run them on Qiskit Aer.")
    sweep = circuits.bb84_sweep(n=200, seed=circuits.PROTOCOL_SEED)
    layout = circuits.bb84_spy_layout(BB84_CLEAN, BB84_EVE)
    bb84 = circuits.bb84_spy_circuit(layout)
    bb84_counts = circuits.aer_counts(bb84, shots=200, seed=11)
    small_layout = circuits.bb84_spy_layout(BB84_CLEAN_SMALL, BB84_EVE_SMALL)
    bb84_small = circuits.bb84_spy_circuit(small_layout)

    grover, grover_meta = circuits.grover_circuit(GROVER_N, GROVER_MARKED)
    grover_counts = circuits.aer_counts(grover, shots=1024, seed=2)
    grover8, grover8_meta = circuits.grover_circuit(8, GROVER8_MARKED)
    grover8_counts = circuits.aer_counts(grover8, shots=1024, seed=3)

    shor = circuits.shor15_circuit(n_count=4)
    shor_counts = circuits.aer_counts(shor, shots=1024, seed=4)
    shor_summary = circuits.analyze_shor(shor_counts, 4)

    teleport = circuits.teleport_circuit()
    teleport_counts = circuits.aer_counts(teleport, shots=1024, seed=5)

    qaoa, qaoa_meta = circuits.optimize_qaoa(shots=256, seed=7)
    qaoa_counts = circuits.aer_counts(qaoa, shots=1024, seed=8)

    clean = next(row for row in sweep if row["eve_fraction"] == 0.0)
    full = next(row for row in sweep if row["eve_fraction"] == 1.0)
    _step(
        trace,
        f"Aer BB84 QBER is {clean['qber']:.3f} with no spy and {full['qber']:.3f} when Eve resends every qubit.",
    )
    _step(
        trace,
        "Aer Shor "
        + (
            f"returned period {shor_summary['period']} and factors {shor_summary['factors']}."
            if shor_summary["period"]
            else "did not accept a period in the top outcomes."
        ),
    )
    return {
        "bb84_sweep": sweep,
        "bb84_rates": circuits.analyze_bb84_counts(bb84_counts, layout),
        "bb84_shots": 200,
        "grover": circuits.analyze_grover(grover_counts, GROVER_MARKED, GROVER_N) | grover_meta,
        "grover_counts": grover_counts,
        "grover8": circuits.analyze_grover(grover8_counts, GROVER8_MARKED, 8) | grover8_meta,
        "grover8_counts": grover8_counts,
        "shor": shor_summary,
        "teleport": circuits.analyze_teleport(teleport_counts),
        "qaoa": circuits.analyze_qaoa(qaoa_counts) | qaoa_meta,
        "payloads": {
            "bb84": {"circuit": bb84, "layout": layout, "qubits": bb84.num_qubits},
            "bb84_small": {"circuit": bb84_small, "layout": small_layout, "qubits": bb84_small.num_qubits},
            "grover": {"circuit": grover, "marked": GROVER_MARKED, "n_items": GROVER_N, "qubits": grover.num_qubits},
            "shor": {"circuit": shor, "n_count": 4, "qubits": shor.num_qubits},
            "teleport": {"circuit": teleport, "qubits": teleport.num_qubits},
            "qaoa": {"circuit": qaoa, "qubits": qaoa.num_qubits},
        },
    }


def _device_rows(devices):
    rows = []
    for device in devices:
        rows.append(
            {
                "qrn": device.qrn,
                "name": device.name,
                "device_type": device.deviceType,
                "paradigm": device.paradigm.value,
                "status": device.status.value,
                "qubits": device.numberQubits,
                "queue_depth": device.queueDepth,
                "noise_models": list(device.noiseModels or []),
                "min_shots": device.minShots,
                "max_shots": device.maxShots,
                "pricing_model": device.pricingModel,
                "pricing": _pricing(device.pricing),
                "direct_access": bool(device.directAccess),
            }
        )
    return rows


def _pick_noise(names):
    for name in NOISE_PREFERENCE:
        if name in names:
            return name
    return names[0] if names else None


def _fit_shots(device, shots):
    if device.minShots:
        shots = max(shots, int(device.minShots))
    if device.maxShots:
        shots = min(shots, int(device.maxShots))
    return shots


def _plan_free(devices, payloads):
    by_qrn = {device.qrn: device for device in devices}
    planned = []

    def add(qrn, key, shots, noise=None):
        device = by_qrn.get(qrn)
        if device is None or device.status.value != "ONLINE":
            return
        payload = payloads[key]
        qubits = device.numberQubits
        if qubits is not None and payload["qubits"] > qubits:
            return
        planned.append(
            {
                "experiment": key if key != "bb84_small" else "bb84",
                "payload_key": key,
                "qrn": qrn,
                "shots": _fit_shots(device, shots),
                "noise_model": noise,
                "kind": _kind(qrn, device.deviceType),
                "qubits": payload["qubits"],
            }
        )

    add("qbraid:qbraid:sim:qir-sv", "bb84", 200)
    add("qbraid:qbraid:sim:qir-sv", "grover", 200)
    add("qbraid:qbraid:sim:qir-sv", "teleport", 200)
    add("qbraid:qbraid:sim:qir-sv", "shor", 256)
    add("qbraid:qbraid:sim:qir-sv", "qaoa", 400)
    ionq = by_qrn.get("ionq:ionq:sim:simulator")
    if ionq is not None:
        noise = _pick_noise(list(ionq.noiseModels or []))
        add("ionq:ionq:sim:simulator", "bb84_small", 200, noise)
        add("ionq:ionq:sim:simulator", "grover", 200, noise)
        add("ionq:ionq:sim:simulator", "teleport", 200, noise)
    add("quantinuum:quantinuum:sim:h2-emulator", "grover", 200)
    add("quantinuum:quantinuum:sim:h2-emulator", "teleport", 200)
    return planned


def _online_qpus(devices):
    chosen = []
    for device in devices:
        if device.deviceType != "QPU" or device.paradigm.value != "gate_model":
            continue
        if device.status.value != "ONLINE":
            continue
        if device.qrn.startswith("openquantum:"):
            continue
        if (device.numberQubits or 0) < 2:
            continue
        chosen.append(device)
    return chosen


def _submit(provider, spec, payloads):
    device = provider.get_device(spec["qrn"])
    program = circuits.for_submission(payloads[spec["payload_key"]]["circuit"])
    kwargs = {
        "shots": spec["shots"],
        "name": f"grid-{spec['experiment']}"[:48],
        "tags": {"demo": "secure-grid", "experiment": spec["experiment"]},
    }
    if spec.get("noise_model"):
        kwargs["runtime_options"] = {"noise_model": spec["noise_model"]}
    job = device.run(program, **kwargs)
    spec = dict(spec)
    spec["job_id"] = job.id
    spec["status"] = "SUBMITTED"
    return job, spec


def _collect(item):
    spec = dict(item["spec"])
    job = item["job"]
    payload = item["payload"]
    try:
        status = job.status()
        spec["status"] = getattr(status, "name", str(status))
        if spec["status"] not in {"COMPLETED", "COMPLETED_WITH_ERRORS"} and not job.is_terminal_state():
            return spec
        result = job.result(timeout=30)
        spec["success"] = bool(getattr(result, "success", spec["status"] == "COMPLETED"))
        if not spec["success"]:
            spec["counts"] = {}
            return spec
        raw = result.data.get_counts()
        counts = _counts_from(raw, spec["shots"])
        spec["counts"] = counts
        analysis = _analyze(spec["experiment"], counts, payload)
        if spec["experiment"] == "bb84":
            spec["rates"] = analysis
        elif spec["experiment"] == "grover":
            spec["grover"] = analysis
        elif spec["experiment"] == "shor":
            spec["shor"] = analysis
        elif spec["experiment"] == "teleport":
            spec["teleport"] = analysis
        elif spec["experiment"] == "qaoa":
            spec["qaoa"] = analysis
        spec["analysis_kind"] = spec["experiment"]
    except Exception as exc:
        spec["status"] = spec.get("status") or "ERROR"
        spec["error"] = f"{type(exc).__name__}: {exc}"
    return spec


def _poll(pending, wait_s, trace):
    deadline = time.time() + wait_s
    records = []
    while pending and time.time() < deadline:
        still = []
        for item in pending:
            try:
                terminal = item["job"].is_terminal_state()
            except Exception as exc:
                spec = dict(item["spec"])
                spec["status"] = "ERROR"
                spec["error"] = f"{type(exc).__name__}: {exc}"
                records.append(spec)
                continue
            if terminal:
                records.append(_collect(item))
            else:
                still.append(item)
        pending = still
        if pending:
            names = ", ".join(item["spec"]["experiment"] + "@" + item["spec"]["qrn"].split(":")[-1] for item in pending)
            _step(trace, f"Waiting on {len(pending)} job(s): {names}")
            time.sleep(8)
    for item in pending:
        spec = dict(item["spec"])
        try:
            status = item["job"].status()
            spec["status"] = getattr(status, "name", str(status))
        except Exception as exc:
            spec["status"] = "UNKNOWN"
            spec["error"] = f"{type(exc).__name__}: {exc}"
        spec["error"] = spec.get("error") or f"still {spec['status']} after {wait_s:.0f}s"
        records.append(spec)
    return records


def run_cloud(local, trace, max_credits, run_hardware, wait_s, use_agent=True, agent_wait=240):
    cloud = {
        "ok": False,
        "jobs": [],
        "devices": [],
        "quotes": [],
        "hardware_decision": "",
        "balance_credits": None,
        "credit_ceiling": max_credits,
    }
    try:
        from qbraid.runtime import GroupJobSession, QbraidProvider

        provider = QbraidProvider()
        devices = list(provider.client.list_devices())
    except Exception as exc:
        cloud["error"] = f"{type(exc).__name__}: {exc}"
        cloud["hardware_decision"] = "Stopped before any job: qBraid did not accept the configured API key."
        _step(trace, cloud["hardware_decision"] + f" ({cloud['error']})")
        return cloud

    cloud["ok"] = True
    cloud["devices"] = _device_rows(devices)
    online = sum(1 for row in cloud["devices"] if row["status"] == "ONLINE")
    _step(trace, f"Listed {len(devices)} qBraid devices, {online} online.")

    try:
        cloud["balance_credits"] = float(provider.client.user_credits_value())
        _step(trace, f"Account balance is {cloud['balance_credits']:.2f} credits.")
    except Exception as exc:
        cloud["balance_error"] = f"{type(exc).__name__}: {exc}"
        _step(trace, "Could not read the credit balance. Paid hardware will not be submitted.")

    payloads = local["payloads"]
    by_qrn = {device.qrn: device for device in devices}
    free_plan = _plan_free(devices, payloads)
    approved = []
    for spec in free_plan:
        quote = _quote(provider.client, spec["qrn"], spec["shots"])
        quote["experiment"] = spec["experiment"]
        quote["role"] = "simulator"
        cloud["quotes"].append(quote)
        allowed, reason = _free_ok(spec["qrn"], quote, by_qrn[spec["qrn"]].pricing)
        spec["quote_reason"] = reason
        spec["estimated_credits"] = quote.get("estimated_credits")
        if allowed:
            approved.append(spec)
        else:
            _step(trace, f"Skip {spec['experiment']} on {spec['qrn']}: {reason}.")

    pending = []
    group_id = None
    if approved:
        _step(trace, f"Submit {len(approved)} free-simulator job(s) in one group.")
        try:
            group = GroupJobSession(
                name="secure-grid-demo",
                tags={"demo": "secure-grid"},
                client=provider.client,
                max_ttl=3600,
            )
            group.open()
            group_id = group.group_id
            cloud["group_id"] = group_id
        except Exception as exc:
            group = None
            cloud["group_error"] = f"{type(exc).__name__}: {exc}"
            _step(trace, f"Group session did not open ({cloud['group_error']}). Submitting jobs one by one.")
        for spec in approved:
            try:
                job, recorded = _submit(provider, spec, payloads)
                pending.append(
                    {"job": job, "spec": recorded, "payload": payloads[recorded["payload_key"]]}
                )
                _step(trace, f"Submitted {recorded['experiment']} to {recorded['qrn']}: {recorded['job_id']}")
            except Exception as exc:
                failed = dict(spec)
                failed["status"] = "REFUSED"
                failed["error"] = f"{type(exc).__name__}: {exc}"
                cloud["jobs"].append(failed)
                _step(trace, f"Refused {spec['experiment']} on {spec['qrn']}: {failed['error']}")
        if group is not None:
            try:
                group.close()
            except Exception as exc:
                cloud["group_close_error"] = f"{type(exc).__name__}: {exc}"

    hardware_notes = []
    if not run_hardware:
        hardware_notes.append("Hardware submission is off (QBRAID_RUN_HARDWARE=0 or --no-hardware).")
    elif cloud["balance_credits"] is None:
        hardware_notes.append("Hardware not submitted because the credit balance could not be read.")
    else:
        ceiling = min(float(max_credits), float(cloud["balance_credits"]))
        cloud["credit_ceiling_applied"] = ceiling
        qpus = _online_qpus(devices)
        if not qpus:
            hardware_notes.append("No online gate-model QPU is available, so no hardware job was submitted.")
        else:
            chosen, all_quotes, leftover = agent_submit.build_hardware_plan(
                qpus,
                payloads,
                lambda qrn, shots: _quote(provider.client, qrn, shots),
                _fit_shots,
                ceiling,
            )
            cloud["quotes"].extend(all_quotes)
            quoted_total = sum(float(row.get("estimated_credits") or 0) for row in chosen)
            cloud["hardware_quoted_credits"] = quoted_total
            cloud["hardware_credits_left"] = leftover
            if not chosen:
                hardware_notes.append(
                    f"No quoted gate-QPU job fits the ceiling of {ceiling:g} credits. Nothing was submitted."
                )
            else:
                programs = RESULTS / "programs"
                rows = agent_submit._write_programs(chosen, payloads, programs)
                plan_path = RESULTS / "hardware_plan.json"
                plan_path.write_text(
                    json.dumps({"max_credits": ceiling, "quoted_credits": quoted_total, "jobs": rows}, indent=2),
                    encoding="utf-8",
                )
                task_path = RESULTS / "agent_task.md"
                task_path.write_text(agent_submit._task_text(rows, ceiling, quoted_total), encoding="utf-8")
                jsonl = RESULTS / "agent_jobs.jsonl"
                jsonl.write_text("", encoding="utf-8")
                _step(
                    trace,
                    f"Hardware plan: {len(rows)} QPU jobs, quoted {quoted_total:.2f} credits, ceiling {ceiling:.2f}.",
                )
                job_ids = {}
                launch = None
                if use_agent:
                    agent_name = "secure-grid-qpu-" + datetime.now(timezone.utc).strftime("%H%M%S")
                    cloud["agent_name"] = agent_name
                    instructions = (
                        "Read results/agent_task.md and submit each command exactly once "
                        "with the qBraid CLI. Append results/agent_jobs.jsonl as that file says. "
                        f"Do not exceed {ceiling:.2f} credits."
                    )
                    try:
                        launch = agent_submit.launch_codeq(ROOT, instructions, agent_name)
                        cloud["agent_launch"] = launch
                        _step(trace, f"Launched qBraid codeq agent {agent_name} to submit the hardware plan.")
                    except Exception as exc:
                        launch = {"returncode": 1, "stderr": f"{type(exc).__name__}: {exc}"}
                        cloud["agent_launch"] = launch
                        _step(trace, f"Agent launch failed ({launch['stderr']}). The script will submit with qbraid jobs submit.")
                    if launch.get("returncode") == 0:
                        found, transcript = agent_submit.collect_agent_submissions(
                            rows, jsonl, agent_name, ROOT, agent_wait, lambda message: _step(trace, message)
                        )
                        job_ids.update(found)
                        cloud["agent_transcript_tail"] = transcript[-2000:]
                        if len(found) < len(rows):
                            hardware_notes.append(
                                f"Agent {agent_name} submitted {len(found)} of {len(rows)} jobs. "
                                "The rest were left unsubmitted so a still-running agent cannot be billed twice. "
                                "Re-run with --cli-submit only if that agent has stopped."
                            )
                    else:
                        hardware_notes.append("codeq did not start. Submitting the same plan with qbraid jobs submit.")
                        for row in rows:
                            try:
                                job_ids[row["name"]] = agent_submit.submit_with_cli(row, ROOT)
                            except Exception as exc:
                                hardware_notes.append(f"CLI refused {row['experiment']} on {row['device']}: {exc}")
                else:
                    _step(trace, "Submitting the hardware plan with qbraid jobs submit (--cli-submit).")
                    for row in rows:
                        try:
                            job_ids[row["name"]] = agent_submit.submit_with_cli(row, ROOT)
                        except Exception as exc:
                            hardware_notes.append(f"CLI refused {row['experiment']} on {row['device']}: {exc}")
                wrapped, submit_notes = agent_submit.jobs_from_ids(provider, rows, job_ids, payloads)
                for item in wrapped:
                    item["spec"]["submitted_by"] = "qbraid-agent" if use_agent and launch and launch.get("returncode") == 0 else "qbraid-cli"
                pending.extend(wrapped)
                hardware_notes.extend(submit_notes)
                for note in submit_notes:
                    _step(trace, note)
    cloud["hardware_decision"] = " ".join(hardware_notes) or "No hardware action."
    if hardware_notes and not any("Submitted" in note for note in hardware_notes):
        _step(trace, cloud["hardware_decision"])

    if pending:
        _step(trace, f"Poll jobs for up to {wait_s:.0f}s.")
        cloud["jobs"].extend(_poll(pending, wait_s, trace))
    finished = sum(1 for job in cloud["jobs"] if job.get("counts"))
    _step(trace, f"Cloud collection finished with counts from {finished} job(s).")
    return cloud


def _write_runs(jobs):
    path = RESULTS / "runs.csv"
    fields = [
        "submitted_utc",
        "experiment",
        "device",
        "kind",
        "job_id",
        "shots",
        "est_credits",
        "status",
        "noise_model",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for job in jobs:
            writer.writerow(
                {
                    "submitted_utc": _now(),
                    "experiment": job.get("experiment", ""),
                    "device": job.get("qrn", ""),
                    "kind": job.get("kind", ""),
                    "job_id": job.get("job_id", ""),
                    "shots": job.get("shots", ""),
                    "est_credits": job.get("estimated_credits", ""),
                    "status": job.get("status", ""),
                    "noise_model": job.get("noise_model") or "",
                }
            )
    return str(path)


def _public_job(job):
    """Drop nothing required for the report, but keep counts: they are the evidence."""
    return job


def write_figures(local, jobs):
    FIGURES.mkdir(parents=True, exist_ok=True)
    written = {}
    written["bb84_sweep"] = figures.save_bb84_sweep(local["bb84_sweep"], FIGURES / "bb84_qber_sweep.png")
    written["bb84_backends"] = figures.save_bb84_backends(
        local["bb84_rates"], jobs, FIGURES / "bb84_clean_vs_spy.png"
    )
    written["grover"] = figures.save_grover(
        local["grover_counts"], GROVER_MARKED, jobs, FIGURES / "grover_search.png"
    )
    written["shor"] = figures.save_shor(
        local["shor"]["phases"], local["shor"].get("factors"), FIGURES / "shor_phases.png"
    )
    written["teleport"] = figures.save_teleport(
        local["teleport"]["q2_zero_frac"], jobs, FIGURES / "teleport_link.png"
    )
    written["qaoa"] = figures.save_qaoa(local["qaoa"], FIGURES / "qaoa_link_selection.png")
    written["overview"] = figures.save_overview(
        local["bb84_sweep"],
        local["grover_counts"],
        GROVER_MARKED,
        local["shor"]["phases"],
        local["teleport"]["q2_zero_frac"],
        FIGURES / "results_overview.png",
    )
    for name, circuit in (
        ("grover_circuit", local["payloads"]["grover"]["circuit"]),
        ("teleport_circuit", local["payloads"]["teleport"]["circuit"]),
    ):
        drawn = figures.draw_circuit(circuit, FIGURES / f"{name}.png", name.replace("_", " "))
        if drawn:
            written[name] = drawn
    return written


def run(local_only=False, max_credits=None, run_hardware=None, wait_s=None, use_agent=None, agent_wait=None):
    RESULTS.mkdir(parents=True, exist_ok=True)
    if max_credits is None:
        max_credits = float(os.environ.get("QBRAID_MAX_CREDITS", "5500"))
    if run_hardware is None:
        run_hardware = os.environ.get("QBRAID_RUN_HARDWARE", "1") != "0"
    if wait_s is None:
        wait_s = float(os.environ.get("QBRAID_WAIT_SECONDS", "900"))
    if use_agent is None:
        use_agent = os.environ.get("QBRAID_USE_AGENT", "1") != "0"
    if agent_wait is None:
        agent_wait = float(os.environ.get("QBRAID_AGENT_SECONDS", "240"))

    trace = []
    _step(trace, "Start the secure-grid qBraid demo.")
    local = run_local(trace)
    cloud = {
        "ok": False,
        "jobs": [],
        "devices": [],
        "quotes": [],
        "hardware_decision": "Cloud and hardware were not requested (--local-only).",
        "balance_credits": None,
        "credit_ceiling": max_credits,
    }
    if not local_only:
        try:
            cloud = run_cloud(
                local, trace, max_credits, run_hardware, wait_s, use_agent=use_agent, agent_wait=agent_wait
            )
        except Exception as exc:
            cloud["error"] = f"{type(exc).__name__}: {exc}"
            cloud["traceback"] = traceback.format_exc(limit=6)
            _step(trace, f"Cloud loop stopped: {cloud['error']}")

    _step(trace, "Draw the figures and write the analysis from the counts that came back.")
    figure_paths = {}
    try:
        figure_paths = write_figures(local, cloud.get("jobs") or [])
        gap = figures.save_qubit_gap(cloud.get("devices") or [], FIGURES / "gate_qpu_qubits.png")
        if gap:
            figure_paths["qpu_gap"] = gap
        elif "qpu_gap" in figure_paths:
            figure_paths.pop("qpu_gap")
    except Exception as exc:
        _step(trace, f"Figure export failed: {type(exc).__name__}: {exc}")

    evidence = {
        "generated_utc": _now(),
        "source": "qhackathon_secure_grid/src notebooks 1, 2, 2b, 3, and the QAOA circuit from 6",
        "credit_ceiling": max_credits,
        "trace": trace,
        "local": {key: value for key, value in local.items() if key != "payloads"},
        "cloud": cloud,
        "figures": figure_paths,
    }
    evidence = _redact(evidence)
    evidence.pop("traceback", None)
    if isinstance(evidence.get("cloud"), dict):
        evidence["cloud"].pop("traceback", None)
    evidence_path = RESULTS / "evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2, default=str), encoding="utf-8")
    runs_path = _write_runs(cloud.get("jobs") or [])
    report_path = write_report(evidence, RESULTS / "ANALYSIS.md")
    print(f"Wrote {report_path}", flush=True)
    print(f"Wrote {evidence_path}", flush=True)
    print(f"Wrote {runs_path}", flush=True)
    return evidence
