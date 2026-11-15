"""Write ANALYSIS.md from one demo run. Every measured number comes from that run."""

from __future__ import annotations

from pathlib import Path


def _pct(value):
    if value is None:
        return "—"
    return f"{100 * float(value):.1f}%"


def _num(value, digits=3):
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _job_line(job):
    device = job.get("qrn", "")
    kind = job.get("kind") or ""
    noise = f", noise {job['noise_model']}" if job.get("noise_model") else ""
    credits = job.get("estimated_credits")
    credit_txt = "—" if credits is None else f"{float(credits):g}"
    return (
        f"| {job.get('experiment', '')} | {kind} | `{device}` | {job.get('shots', '')} "
        f"| {credit_txt} | {job.get('status', '')} | `{job.get('job_id', '')}` |{noise and ' ' + noise or ''}"
    )


def _bb84_section(local, jobs):
    sweep = local.get("bb84_sweep") or []
    lines = [
        "## BB84",
        "",
        "Each point is 200 qubits on the local Aer simulator. Eve measures that fraction in a random basis and resends. "
        "The error rate is only on rounds where Alice and Bob picked the same basis. "
        "The gray line in the figure is 0.25 times Eve's fraction, the usual intercept-resend average.",
        "",
        "| Eve fraction | Sifted bits | Errors | QBER |",
        "|---:|---:|---:|---:|",
    ]
    first_cross = None
    for row in sweep:
        lines.append(
            f"| {row['eve_fraction']:.1f} | {row['sifted']} | {row['errors']} | {row['qber']:.3f} |"
        )
        if first_cross is None and row["qber"] >= 0.11:
            first_cross = row
    clean = next((row for row in sweep if row["eve_fraction"] == 0.0), None)
    full = next((row for row in sweep if row["eve_fraction"] == 1.0), None)
    lines.append("")
    if clean and full:
        lines.append(
            f"With no spy the sifted error rate was {clean['qber']:.3f} "
            f"({clean['errors']} errors in {clean['sifted']} sifted bits). "
            f"With Eve on every qubit it was {full['qber']:.3f} "
            f"({full['errors']} of {full['sifted']})."
        )
    if first_cross:
        lines.append(
            f"In this sample the error rate first reached the 11% one-way security bound at "
            f"Eve fraction {first_cross['eve_fraction']:.1f} (QBER {first_cross['qber']:.3f}). "
            "That 11% line is the Shor–Preskill one-way bound, not a field alarm setting."
        )
    else:
        lines.append("This sample did not reach an 11% sifted error rate.")
    rates = local.get("bb84_rates") or {}
    lines.extend(
        [
            "",
            "A second circuit puts clean rounds and an in-circuit spy on one chip so the same program can be sent to a simulator or a QPU. "
            f"On Aer ({local.get('bb84_shots', '—')} shots, {rates.get('qubits', '—')} qubits) the clean-round error rate was "
            f"{_num(rates.get('clean'))} and the spy-round error rate was {_num(rates.get('eve_all'))}.",
            "",
            "| Backend | Kind | Clean error | Spy error | Shots | Job |",
            "|---|---|---:|---:|---:|---|",
            f"| Aer | simulator | {_num(rates.get('clean'))} | {_num(rates.get('eve_all'))} | {local.get('bb84_shots', '')} | local |",
        ]
    )
    for job in jobs:
        if job.get("analysis_kind") != "bb84" or not job.get("rates"):
            continue
        got = job["rates"]
        lines.append(
            f"| `{job.get('qrn', '')}` | {job.get('kind', '')} | {_num(got.get('clean'))} | "
            f"{_num(got.get('eve_all'))} | {job.get('shots', '')} | `{job.get('job_id', '')}` |"
        )
    lines.append("")
    return lines


def _shor_section(local, jobs):
    shor = local.get("shor") or {}
    factors = shor.get("factors")
    factor_txt = " and ".join(str(x) for x in factors) if factors else "none"
    lines = [
        "## Shor, factoring 15",
        "",
        f"The local run used {shor.get('n_count', '—')} counting qubits and {shor.get('shots', '—')} shots. "
        "The multiply-by-7-mod-15 step is the notebook's hand-built gate. It does not factor a general RSA modulus. "
        "The notebook's longer register is 8 counting qubits; 4 counting qubits already resolve the period 4.",
        "",
        f"Accepted period: {shor.get('period') if shor.get('period') is not None else 'none'}. "
        f"Factors of 15 from that period: {factor_txt}.",
        "",
    ]
    tried = shor.get("tried") or []
    if tried:
        lines.extend(
            [
                "| Bitstring | Counts | Phase | Candidate period | 7^r mod 15 | Used |",
                "|---|---:|---:|---:|---:|---|",
            ]
        )
        for row in tried:
            lines.append(
                f"| `{row['bitstring']}` | {row['counts']} | {row['phase']:.4f} | {row['period']} | "
                f"{row['seven_pow_mod']} | {'yes' if row['accepted'] else 'no'} |"
            )
        lines.append("")
    for job in jobs:
        if job.get("analysis_kind") != "shor" or not job.get("shor"):
            continue
        got = job["shor"]
        fac = got.get("factors")
        fac_txt = " and ".join(str(x) for x in fac) if fac else "none"
        lines.append(
            f"`{job.get('qrn')}` ({job.get('kind')}, job `{job.get('job_id')}`, {job.get('shots')} shots) "
            f"accepted period {got.get('period')} and factors {fac_txt}."
        )
    if any(job.get("analysis_kind") == "shor" and job.get("shor") for job in jobs):
        lines.append("")
    return lines


def _grover_section(local, jobs):
    def block(title, row):
        if not row:
            return []
        return [
            f"{title}: marked key {row.get('marked')}, {row.get('iterations')} iteration(s), "
            f"{row.get('shots')} shots. Success probability {_pct(row.get('success_prob'))} "
            f"against a uniform {_pct(row.get('uniform_prob'))}. "
            f"Most common key {row.get('top_key')} ({'the marked key' if row.get('found') else 'not the marked key'})."
        ]

    lines = ["## Grover", ""]
    lines.extend(block("Aer, N = 4", local.get("grover")))
    lines.append("")
    lines.extend(block("Aer, N = 8", local.get("grover8")))
    lines.append("")
    lines.append("| Backend | Kind | Success | Shots | Top key | Job |")
    lines.append("|---|---|---:|---:|---:|---|")
    grover = local.get("grover") or {}
    lines.append(
        f"| Aer | simulator | {_pct(grover.get('success_prob'))} | {grover.get('shots', '')} | "
        f"{grover.get('top_key', '')} | local |"
    )
    for job in jobs:
        if job.get("analysis_kind") != "grover" or not job.get("grover"):
            continue
        got = job["grover"]
        lines.append(
            f"| `{job.get('qrn')}` | {job.get('kind')} | {_pct(got.get('success_prob'))} | "
            f"{job.get('shots')} | {got.get('top_key')} | `{job.get('job_id')}` |"
        )
    lines.append("")
    return lines


def _teleport_section(local, jobs):
    tele = local.get("teleport") or {}
    lines = [
        "## Teleportation link",
        "",
        "The circuit is the notebook's three-qubit teleport. Corrections are gates. "
        "Undoing the prepared state on qubit 2 should leave |0>, which is the left-most bit in Qiskit's print order.",
        "",
        f"Aer: qubit 2 read 0 on {tele.get('q2_zero', '—')} of {tele.get('shots', '—')} shots "
        f"({_pct(tele.get('q2_zero_frac'))}).",
        "",
    ]
    margins = tele.get("margins") or []
    if margins:
        bits = ", ".join(f"qubit {row['qubit']} was 0 on {_pct(row['prob_zero'])} of shots" for row in margins)
        lines.append(f"Aer marginals: {bits}. Qubits 0 and 1 are the Bell measurement and should stay mixed.")
        lines.append("")
    lines.extend(
        [
            "| Backend | Kind | Qubit 2 = 0 | Shots | Job |",
            "|---|---|---:|---:|---|",
            f"| Aer | simulator | {_pct(tele.get('q2_zero_frac'))} | {tele.get('shots', '')} | local |",
        ]
    )
    for job in jobs:
        if job.get("analysis_kind") != "teleport" or not job.get("teleport"):
            continue
        got = job["teleport"]
        lines.append(
            f"| `{job.get('qrn')}` | {job.get('kind')} | {_pct(got.get('q2_zero_frac'))} | "
            f"{job.get('shots')} | `{job.get('job_id')}` |"
        )
    lines.append("")
    return lines


def _qaoa_section(local, jobs):
    qaoa = local.get("qaoa") or {}
    exact = qaoa.get("exact") or {}
    greedy = qaoa.get("greedy") or {}
    best = qaoa.get("qaoa_best_feasible") or {}
    lines = [
        "## QKD link selection",
        "",
        "Notebook 6 compares greedy, exact search, and one QAOA layer. "
        "This run uses four links with equal cost 10 and a budget of 20, so the exact answer is the two highest-value links. "
        "The 16-link city instance stays in the notebook; four qubits fit a free simulator and a small QPU.",
        "",
        f"Greedy value {greedy.get('value', '—')} on {', '.join(greedy.get('links') or []) or '—'}.",
        f"Exact value {exact.get('value', '—')} on {', '.join(exact.get('links') or []) or '—'}.",
    ]
    if best:
        lines.append(
            f"Best feasible QAOA sample value {best.get('value')} on {', '.join(best.get('links') or []) or '—'} "
            f"(probability of that bitstring { _pct(best.get('prob')) }). "
            f"It {'matches' if qaoa.get('matches_exact') else 'does not match'} the exact set. "
            f"Probability of the exact bitstring `{qaoa.get('optimal_bitstring')}` was {_pct(qaoa.get('optimal_prob'))} "
            f"in {qaoa.get('shots')} Aer shots. Training used gamma { _num(qaoa.get('gamma')) } and beta { _num(qaoa.get('beta')) }."
        )
    lines.append("")
    for job in jobs:
        if job.get("analysis_kind") != "qaoa" or not job.get("qaoa"):
            continue
        got = job["qaoa"]
        sampled = got.get("qaoa_best_feasible") or {}
        lines.append(
            f"`{job.get('qrn')}` ({job.get('kind')}, job `{job.get('job_id')}`, {job.get('shots')} shots) "
            f"best feasible value {sampled.get('value', '—')} "
            f"on {', '.join(sampled.get('links') or []) or '—'}; "
            f"exact-bitstring probability {_pct(got.get('optimal_prob'))}."
        )
    if any(job.get("analysis_kind") == "qaoa" and job.get("qaoa") for job in jobs):
        lines.append("")
    return lines


def _cloud_section(cloud):
    lines = ["## Devices, quotes, and jobs", ""]
    decision = cloud.get("hardware_decision") or ""
    if decision:
        lines.append(decision)
        lines.append("")
    if cloud.get("error"):
        lines.append(f"Cloud loop error: {cloud['error']}")
        lines.append("")
    if cloud.get("balance_credits") is not None:
        lines.append(
            f"Credit balance read for this run: {float(cloud['balance_credits']):.2f}. "
            f"Ceiling: {cloud.get('credit_ceiling')} credits."
        )
        lines.append("")
    if cloud.get("group_id"):
        lines.append(f"Free-simulator group: `{cloud['group_id']}`.")
        lines.append("")
    devices = cloud.get("devices") or []
    if devices:
        online = [d for d in devices if d.get("status") == "ONLINE"]
        qpus = [d for d in online if d.get("device_type") == "QPU" and d.get("paradigm") == "gate_model"]
        qpus.sort(key=lambda d: (-(d.get("qubits") or 0), d.get("qrn") or ""))
        lines.append(
            f"The account listed {len(devices)} devices, {len(online)} online, "
            f"{len(qpus)} of them online gate-model QPUs."
        )
        if qpus:
            largest = qpus[0]
            lines.append(
                f"Largest online gate-model QPU in this listing: {largest.get('name')} "
                f"(`{largest.get('qrn')}`), {largest.get('qubits')} qubits."
            )
            lines.extend(["", "| Online gate QPU | Qubits | Queue |", "|---|---:|---:|"])
            for device in qpus:
                lines.append(
                    f"| `{device.get('qrn')}` | {device.get('qubits')} | {device.get('queue_depth')} |"
                )
            lines.append("")
    quotes = cloud.get("quotes") or []
    paid = [q for q in quotes if q.get("role") == "qpu"]
    if paid:
        lines.extend(
            [
                "Hardware quotes from `estimate_cost`, before any QPU submission:",
                "",
                "| Device | Shots | Quote (credits) | Priced |",
                "|---|---:|---:|---|",
            ]
        )
        seen = set()
        for quote in paid:
            key = (quote.get("qrn"), quote.get("shots"), quote.get("experiment"))
            if key in seen:
                continue
            seen.add(key)
            cost = quote.get("estimated_credits")
            cost_txt = "—" if cost is None else f"{float(cost):g}"
            lines.append(
                f"| `{quote.get('qrn')}` ({quote.get('experiment')}) | {quote.get('shots')} | {cost_txt} | "
                f"{'yes' if quote.get('pricing_available') else 'no'} |"
            )
        lines.append("")
    jobs = cloud.get("jobs") or []
    if jobs:
        lines.extend(
            [
                "| Experiment | Kind | Device | Shots | Quote | Status | Job |",
                "|---|---|---|---:|---:|---|---|",
            ]
        )
        for job in jobs:
            credits = job.get("estimated_credits")
            credit_txt = "—" if credits is None else f"{float(credits):g}"
            note = ""
            if job.get("noise_model"):
                note = f" noise `{job['noise_model']}`"
            if job.get("error") and job.get("status") != "COMPLETED":
                note += f" {job['error']}"
            lines.append(
                f"| {job.get('experiment')} | {job.get('kind')} | `{job.get('qrn')}` | {job.get('shots')} | "
                f"{credit_txt} | {job.get('status')}{note} | `{job.get('job_id', '')}` |"
            )
        lines.append("")
        waiting = [job for job in jobs if job.get("job_id") and not job.get("counts") and job.get("kind") == "qpu"]
        for job in waiting:
            lines.append(
                f"Hardware job `{job.get('job_id')}` on `{job.get('qrn')}` was still {job.get('status')} "
                "when polling stopped. No counts from that job are included above."
            )
        if waiting:
            lines.append("")
    elif not cloud.get("error"):
        lines.append("No cloud job was submitted.")
        lines.append("")
    return lines


def write_report(evidence, path: Path):
    local = evidence.get("local") or {}
    cloud = evidence.get("cloud") or {}
    jobs = cloud.get("jobs") or []
    lines = [
        "# Secure-grid demo results",
        "",
        f"Generated {evidence.get('generated_utc', '')}.",
        "",
        "Programs come from the notebooks in `src`: BB84, Shor's factoring of 15, Grover search, teleportation, "
        "and the QAOA link-selection circuit. The agent runs them on local Aer, quotes qBraid, submits free simulators "
        "only when `estimate_cost` returns 0 credits, and submits a gate-model QPU only when the quote fits the credit ceiling and the balance.",
        "",
        "Emulator results are emulator results. They are not QPU results. "
        "A QPU error rate here is the processor's error on this circuit, not the error rate of a utility fiber.",
        "",
        "## Steps",
        "",
    ]
    for step in evidence.get("trace") or []:
        lines.append(f"- {step.get('utc', '')}: {step.get('message', '')}")
    lines.append("")
    lines.extend(_bb84_section(local, jobs))
    lines.extend(_shor_section(local, jobs))
    lines.extend(_grover_section(local, jobs))
    lines.extend(_teleport_section(local, jobs))
    lines.extend(_qaoa_section(local, jobs))
    lines.extend(_cloud_section(cloud))
    figures = evidence.get("figures") or {}
    if figures:
        lines.extend(["## Figures", ""])
        for name, figure_path in figures.items():
            lines.append(f"- {name}: `{figure_path}`")
        lines.append("")
    lines.extend(
        [
            "## What this run does not show",
            "",
            "BB84 here is a circuit experiment, not a fiber QKD link. The notebook does not do error correction or privacy amplification, and neither does this demo. "
            "Shor's gate is hardcoded for 15. Grover's oracle is the known key, not AES. "
            "The QAOA instance is four links, not the city network in notebook 6.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)
