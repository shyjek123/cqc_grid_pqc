"""Figures for the simulator, cloud, and hardware comparison."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import numpy as np

# Okabe-Ito, so the bars stay distinct in print and for color-blind readers.
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
VERMILION = "#D55E00"
SKY = "#56B4E9"
PURPLE = "#CC79A7"
INK = "#222222"

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "medium",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
    }
)


def _finish(fig, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return str(path)


def _backend_label(job):
    device = job.get("device", "")
    kind = job.get("kind", "")
    short = device.split(":")[-1]
    if kind == "qpu":
        return f"QPU {short}"
    if "emulator" in device:
        return f"emulator {short}"
    if job.get("noise_model"):
        return f"{short}\n({job['noise_model']})"
    return short


def save_bb84_sweep(sweep, path: Path):
    fractions = [row["eve_fraction"] for row in sweep]
    qber = [row["qber"] for row in sweep]
    errors = []
    for row in sweep:
        p, n = row["qber"], row["sifted"]
        errors.append(float(np.sqrt(p * (1 - p) / n)) if n else 0.0)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(fractions, [0.25 * f for f in fractions], color="#888888", lw=1.5, label="0.25 × fraction Eve touches")
    ax.errorbar(
        fractions,
        qber,
        yerr=errors,
        fmt="o",
        color=VERMILION,
        ecolor=VERMILION,
        capsize=3,
        label="Aer, 200 qubits",
    )
    ax.axhline(0.11, color=INK, ls="--", lw=1, label="11% one-way bound")
    ax.set_xlabel("Fraction of qubits Eve measures and resends")
    ax.set_ylabel("Sifted-key error rate")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 0.45)
    ax.set_title("BB84: a fuller intercept-resend leaves more errors")
    ax.legend(frameon=False, fontsize=9)
    return _finish(fig, path)


def save_bb84_backends(local_rates, jobs, path: Path):
    rows = [("Aer", local_rates)]
    for job in jobs:
        if job.get("analysis_kind") == "bb84" and job.get("rates"):
            rows.append((_backend_label(job), job["rates"]))
    labels = [name for name, _ in rows]
    clean = [r.get("clean") or 0 for _, r in rows]
    eve = [r.get("eve_all") or 0 for _, r in rows]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(max(7.0, 1.6 * len(labels) + 2), 4.3))
    ax.bar(x - 0.18, clean, width=0.36, color=BLUE, label="Clean rounds")
    ax.bar(x + 0.18, eve, width=0.36, color=VERMILION, label="Spy rounds")
    ax.axhline(0.25, color="#888888", ls=":", lw=1, label="25% intercept-resend")
    ax.set_xticks(x, labels, fontsize=8)
    ax.set_ylabel("Error rate")
    ax.set_ylim(0, 0.55)
    ax.set_title("Same BB84 circuit, clean rounds beside an in-circuit spy")
    ax.legend(frameon=False, fontsize=9, ncol=3)
    return _finish(fig, path)


def save_grover(local_counts, marked, jobs, path: Path):
    from qbraid.visualization import plot_distribution

    series = [("Aer", local_counts)]
    for job in jobs:
        if job.get("analysis_kind") == "grover" and job.get("counts") and job.get("qubits", 2) == 2:
            series.append((_backend_label(job).replace("\n", " "), job["counts"]))
    # Four states already fill the axis. Extra backends go in the written comparison.
    series = series[:4]
    fig = plt.figure(figsize=(8.4, 4.4))
    plot_distribution(
        [counts for _, counts in series],
        legend=[name for name, _ in series],
        title=f"Grover search for key {marked} (N = 4)",
        x_label="Measured bitstring (Qiskit order)",
        y_label="Probability",
        show_plot=False,
        save_path=None,
    )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return str(path)


def save_shor(phases, factors, path: Path):
    items = sorted(((float(k), v) for k, v in phases.items()), key=lambda kv: kv[0])
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar([f"{p:.3f}" for p, _ in items], [c for _, c in items], color=BLUE)
    label = "factors " + " × ".join(str(x) for x in factors) if factors else "no factor found"
    ax.set_xlabel("Measured phase")
    ax.set_ylabel("Counts")
    ax.set_title(f"Shor demo, 7^x mod 15 — {label}")
    ax.tick_params(axis="x", labelrotation=45)
    return _finish(fig, path)


def save_teleport(local_frac, jobs, path: Path):
    labels = ["Aer"]
    values = [local_frac]
    for job in jobs:
        if job.get("analysis_kind") == "teleport" and job.get("teleport"):
            labels.append(_backend_label(job))
            values.append(job["teleport"]["q2_zero_frac"])
    fig, ax = plt.subplots(figsize=(max(6.5, 1.4 * len(labels) + 2), 4.2))
    colors = [BLUE] + [ORANGE] * (len(labels) - 1)
    ax.bar(np.arange(len(labels)), values, color=colors[: len(labels)])
    ax.axhline(1.0, color=GREEN, ls="--", lw=1, label="Qubit 2 is |0> on every shot")
    ax.set_xticks(np.arange(len(labels)), labels, fontsize=8)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Fraction of shots with qubit 2 = 0")
    ax.set_title("Teleportation check: the received qubit undoes to |0>")
    ax.legend(frameon=False, fontsize=9)
    return _finish(fig, path)


def save_qaoa(qaoa, path: Path):
    exact = qaoa["exact"]["value"]
    greedy = qaoa["greedy"]["value"]
    sampled = (qaoa.get("qaoa_best_feasible") or {}).get("value", 0)
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.bar(
        ["Greedy", "Exact", "QAOA sample"],
        [greedy, exact, sampled],
        color=[SKY, GREEN, PURPLE],
    )
    ax.set_ylabel("Total link value under the budget")
    ax.set_title("Which links get QKD: greedy, exact, one QAOA layer")
    for i, value in enumerate((greedy, exact, sampled)):
        ax.text(i, value + 0.8, f"{value:.0f}", ha="center", fontsize=10)
    ax.set_ylim(0, max(exact, greedy, sampled) * 1.18)
    return _finish(fig, path)


def save_qubit_gap(devices, path: Path):
    qpus = []
    seen = set()
    for device in devices:
        if device.get("device_type") != "QPU":
            continue
        if device.get("paradigm") != "gate_model":
            continue
        name = device.get("name") or device["qrn"]
        qubits = device.get("qubits")
        if not qubits:
            continue
        key = (name, qubits)
        if key in seen:
            continue
        seen.add(key)
        qpus.append((qubits, name))
    if not qpus:
        return None
    qpus.sort()
    fig, ax = plt.subplots(figsize=(8.0, max(3.8, 0.32 * len(qpus) + 1.2)))
    ax.barh([name for _, name in qpus], [q for q, _ in qpus], color=BLUE)
    largest = qpus[-1][0]
    ax.set_xlabel("Qubits")
    ax.set_title(f"Gate-model QPUs on this account (largest {largest})")
    return _finish(fig, path)


def save_overview(sweep, grover_counts, marked, shor_phases, teleport_frac, path: Path):
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))
    fractions = [row["eve_fraction"] for row in sweep]
    axes[0, 0].plot(fractions, [row["qber"] for row in sweep], "o-", color=VERMILION)
    axes[0, 0].plot(fractions, [0.25 * f for f in fractions], color="#888888", lw=1)
    axes[0, 0].axhline(0.11, color=INK, ls="--", lw=0.8)
    axes[0, 0].set_title("BB84 error vs spy fraction")
    axes[0, 0].set_ylabel("QBER")

    keys = sorted(grover_counts)
    axes[0, 1].bar(keys, [grover_counts[k] for k in keys], color=BLUE)
    axes[0, 1].set_title(f"Grover N=4, marked {marked:02b}")
    axes[0, 1].tick_params(axis="x", labelrotation=0)
    axes[0, 1].set_ylabel("Counts")

    items = sorted(((float(k), v) for k, v in shor_phases.items()), key=lambda kv: kv[0])
    axes[1, 0].bar([f"{p:.2f}" for p, _ in items], [c for _, c in items], color=GREEN)
    axes[1, 0].set_title("Shor phases for 7^x mod 15")
    axes[1, 0].tick_params(axis="x", labelrotation=45)
    axes[1, 0].set_ylabel("Counts")

    axes[1, 1].bar(["qubit 2 = 0"], [teleport_frac], color=ORANGE)
    axes[1, 1].set_ylim(0, 1.05)
    axes[1, 1].set_title("Teleport check on Aer")
    axes[1, 1].set_ylabel("Fraction of shots")
    return _finish(fig, path)


def draw_circuit(circuit, path: Path, title: str):
    try:
        figure = circuit.draw(output="mpl", fold=-1)
        if figure is None:
            return None
        figure.suptitle(title, fontsize=12)
        return _finish(figure, path)
    except Exception:
        plt.close("all")
        return None
