"""Quantum programs extracted from ``qhackathon_secure_grid/src``.

Notebooks 1, 2, 2b, and 3 supply BB84, Shor's factoring of 15, Grover search,
and teleportation. Notebook 6 supplies the QAOA cost/mixer circuit used to pick
QKD links. The city-network notebooks (4 and 5) call the separate ``secure_grid``
package; the link-selection demo below is the quantum piece of notebook 6, cut
to four links so a free simulator and a small QPU can run the same circuit.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Same seed the BB84 notebook uses for Alice's bits and bases.
PROTOCOL_SEED = 42
CHUNK = 16


def encode(bit, basis):
    """Prepare Alice's bit as a one-qubit circuit in the basis she chose.

    The X gate sets the bit. Basis 0 stays in Z; basis 1 adds H for the X basis.
    Extracted from ``1_bb84_eavesdropper.ipynb``.
    """
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == 1:
        qc.h(0)
    return qc


def _prepare(qc, q, bit, basis):
    if int(bit) == 1:
        qc.x(q)
    if int(basis) == 1:
        qc.h(q)


def _chunk_measure(bits, prep_bases, meas_bases, seed):
    """Measure each qubit once. Same gates as ``encode`` plus Bob's basis change.

    Chunked at 16 qubits. The rounds are a product state, and a 200-qubit
    statevector will not fit in memory.
    """
    sim = AerSimulator()
    rng = np.random.default_rng(seed)
    bits = np.asarray(bits, dtype=int)
    prep_bases = np.asarray(prep_bases, dtype=int)
    meas_bases = np.asarray(meas_bases, dtype=int)
    out = np.empty(len(bits), dtype=int)
    for start in range(0, len(bits), CHUNK):
        stop = min(start + CHUNK, len(bits))
        k = stop - start
        qc = QuantumCircuit(k, k)
        for q in range(k):
            _prepare(qc, q, bits[start + q], prep_bases[start + q])
            if meas_bases[start + q] == 1:
                qc.h(q)
        qc.measure(range(k), range(k))
        seed_sim = int(rng.integers(1, 2**31 - 1))
        counts = sim.run(qc, shots=1, seed_simulator=seed_sim).result().get_counts()
        bitstring = next(iter(counts))
        out[start:stop] = [int(c) for c in bitstring[::-1]]
    return out


def bb84_sample(n, eve_fraction, seed):
    """One intercept-resend sample. Eve measures ``eve_fraction`` of the qubits and resends.

    Sifting keeps the rounds where Alice and Bob chose the same basis. The error
    rate is on those rounds only, which is the notebook's ``qber``.
    """
    rng = np.random.default_rng(seed)
    alice_bits = rng.integers(0, 2, n)
    alice_bases = rng.integers(0, 2, n)
    bob_bases = rng.integers(0, 2, n)
    tapped = rng.random(n) < float(eve_fraction)
    if np.any(tapped):
        eve_bases = rng.integers(0, 2, n)
        eve_bits = _chunk_measure(alice_bits, alice_bases, eve_bases, seed + 17)
        sent_bits = np.where(tapped, eve_bits, alice_bits)
        sent_bases = np.where(tapped, eve_bases, alice_bases)
    else:
        sent_bits, sent_bases = alice_bits, alice_bases
    bob_bits = _chunk_measure(sent_bits, sent_bases, bob_bases, seed + 91)
    keep = alice_bases == bob_bases
    sifted = int(np.count_nonzero(keep))
    errors = int(np.count_nonzero(alice_bits[keep] != bob_bits[keep])) if sifted else 0
    qber = errors / sifted if sifted else 0.0
    return {
        "n": int(n),
        "eve_fraction": float(eve_fraction),
        "qber": float(qber),
        "errors": errors,
        "sifted": sifted,
        "seed": int(seed),
    }


def bb84_sweep(n=200, seed=PROTOCOL_SEED):
    """QBER from no spy through a full intercept-resend, in steps of 10%."""
    rows = []
    for i, fraction in enumerate(np.round(np.linspace(0.0, 1.0, 11), 2)):
        rows.append(bb84_sample(n, float(fraction), seed + 1000 * i))
    return rows


def bb84_spy_layout(n_clean=8, n_eve=4):
    """Balanced rounds for one circuit. Bob measures in Alice's basis, so every shot is sifted.

    Half of Eve's probes use Alice's basis and half use the other basis. Extracted
    from the hardware-layout pattern used with the BB84 notebook.
    """
    states = [(0, 0), (1, 0), (0, 1), (1, 1)]
    clean = [states[i % 4] for i in range(n_clean)]
    eve = []
    for i in range(n_eve):
        bit, basis = states[i % 4]
        eve_basis = basis if i % 2 == 0 else 1 - basis
        eve.append((bit, basis, eve_basis))
    return {"clean": clean, "eve": eve}


def bb84_spy_circuit(layout):
    """Clean rounds and in-circuit intercept-resend rounds, then one measurement."""
    n_clean, n_eve = len(layout["clean"]), len(layout["eve"])
    n = n_clean + 2 * n_eve
    qc = QuantumCircuit(n, n)
    for q, (bit, basis) in enumerate(layout["clean"]):
        _prepare(qc, q, bit, basis)
        if basis:
            qc.h(q)
    for i, (bit, basis, eve_basis) in enumerate(layout["eve"]):
        sig, probe = n_clean + i, n_clean + n_eve + i
        _prepare(qc, sig, bit, basis)
        if eve_basis:
            qc.h(sig)
        qc.cx(sig, probe)
        if eve_basis:
            qc.h(sig)
        if basis:
            qc.h(sig)
    qc.measure(range(n), range(n))
    return qc


def analyze_bb84_counts(counts, layout):
    """Error rates for clean rounds and spy rounds. Qiskit prints qubit 0 last."""
    n_clean, n_eve = len(layout["clean"]), len(layout["eve"])
    n = n_clean + 2 * n_eve
    tally = {
        "clean": [0, 0],
        "eve_same_basis": [0, 0],
        "eve_other_basis": [0, 0],
    }
    for bitstring, c in counts.items():
        bits = str(bitstring).replace(" ", "").zfill(n)[::-1]
        c = int(c)
        for q, (bit, _) in enumerate(layout["clean"]):
            tally["clean"][0] += c * (int(bits[q]) != bit)
            tally["clean"][1] += c
        for i, (bit, basis, eve_basis) in enumerate(layout["eve"]):
            group = "eve_same_basis" if eve_basis == basis else "eve_other_basis"
            tally[group][0] += c * (int(bits[n_clean + i]) != bit)
            tally[group][1] += c
    rates = {}
    for key, (hits, total) in tally.items():
        rates[key] = (hits / total) if total else None
        rates[f"{key}_hits"] = hits
        rates[f"{key}_total"] = total
    eve_hits = tally["eve_same_basis"][0] + tally["eve_other_basis"][0]
    eve_total = tally["eve_same_basis"][1] + tally["eve_other_basis"][1]
    rates["eve_all"] = (eve_hits / eve_total) if eve_total else None
    rates["qubits"] = n
    return rates


def c_amod15_a7(power):
    """Controlled multiply by 7^power mod 15. Extracted from ``2_shor_harvest_now.ipynb``.

    A real RSA number needs a general modular multiply. This gate is only for 15.
    """
    gate = QuantumCircuit(4)
    for _ in range(power):
        gate.swap(0, 1)
        gate.swap(1, 2)
        gate.swap(2, 3)
        for q in range(4):
            gate.x(q)
    controlled = gate.to_gate()
    controlled.name = f"7^{power} mod 15"
    return controlled.control()


def qft_dagger(n):
    """Inverse Fourier transform on the counting qubits."""
    qc = QuantumCircuit(n)
    for q in range(n // 2):
        qc.swap(q, n - q - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / 2 ** (j - m), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc


def shor15_circuit(n_count=8):
    """Phase estimation of multiply-by-7 mod 15. ``n_count`` is the notebook's 8."""
    qc = QuantumCircuit(n_count + 4, n_count)
    qc.h(range(n_count))
    qc.x(n_count)
    for i in range(n_count):
        qc.append(c_amod15_a7(2**i), [i] + list(range(n_count, n_count + 4)))
    qc.append(qft_dagger(n_count), range(n_count))
    qc.measure(range(n_count), range(n_count))
    return qc


def analyze_shor(counts, n_count):
    """Continue from the most common bitstring until the period check passes."""
    ranked = sorted(counts, key=counts.get, reverse=True)
    tried = []
    chosen = None
    for measured in ranked:
        phase = int(str(measured), 2) / (2**n_count)
        r = Fraction(phase).limit_denominator(15).denominator
        good = r % 2 == 0 and r > 0 and pow(7, r, 15) == 1
        tried.append(
            {
                "bitstring": str(measured),
                "counts": int(counts[measured]),
                "phase": phase,
                "period": int(r),
                "seven_pow_mod": int(pow(7, r, 15)),
                "accepted": bool(good and chosen is None),
            }
        )
        if good and chosen is None:
            chosen = int(r)
            if len(tried) >= 8:
                break
        if len(tried) >= 8 and chosen is not None:
            break
    factors = None
    if chosen:
        factors = sorted(
            [int(gcd(7 ** (chosen // 2) - 1, 15)), int(gcd(7 ** (chosen // 2) + 1, 15))]
        )
    phase_hist = {}
    total = 0
    for bitstring, c in counts.items():
        phase = int(str(bitstring), 2) / (2**n_count)
        key = f"{phase:.6f}".rstrip("0").rstrip(".")
        phase_hist[key] = phase_hist.get(key, 0) + int(c)
        total += int(c)
    return {
        "n_count": int(n_count),
        "shots": total,
        "tried": tried[:8],
        "period": chosen,
        "factors": factors,
        "factored_15": factors == [3, 5] or factors == [5, 3],
        "phases": phase_hist,
    }


def mcz(qc, qubits):
    """Minus sign on |11...1|. Hadamards turn the bit flip into a sign flip."""
    *ctrl, tgt = list(qubits)
    qc.h(tgt)
    qc.mcx(ctrl, tgt)
    qc.h(tgt)


def oracle(qc, qubits, marked):
    """Phase-flip the secret key. Extracted from ``2b_grover_symmetric_keys.ipynb``."""
    bits = format(marked, f"0{len(qubits)}b")[::-1]
    for i, b in enumerate(bits):
        if b == "0":
            qc.x(qubits[i])
    mcz(qc, qubits)
    for i, b in enumerate(bits):
        if b == "0":
            qc.x(qubits[i])


def diffusion(qc, qubits):
    """Reflect every amplitude about the average."""
    qc.h(qubits)
    qc.x(qubits)
    mcz(qc, qubits)
    qc.x(qubits)
    qc.h(qubits)


def grover_circuit(n_items, marked):
    """Grover search. Iterations are floor(pi/4 * sqrt(N)), as in the notebook."""
    n = int(np.log2(n_items))
    iterations = int(np.floor((np.pi / 4) * np.sqrt(n_items)))
    qc = QuantumCircuit(n, n)
    qubits = list(range(n))
    qc.h(qubits)
    for _ in range(iterations):
        oracle(qc, qubits, marked)
        diffusion(qc, qubits)
    qc.measure(qubits, qubits)
    return qc, {"n_items": int(n_items), "qubits": n, "marked": int(marked), "iterations": iterations}


def analyze_grover(counts, marked, n_items):
    total = sum(int(v) for v in counts.values()) or 1
    hits = 0
    top_key, top_count = None, -1
    width = int(np.log2(n_items))
    for bitstring, c in counts.items():
        c = int(c)
        if int(str(bitstring).replace(" ", ""), 2) == int(marked):
            hits += c
        if c > top_count:
            top_key, top_count = str(bitstring).replace(" ", ""), c
    return {
        "marked": int(marked),
        "marked_bitstring": format(int(marked), f"0{width}b"),
        "success_count": hits,
        "shots": total,
        "success_prob": hits / total,
        "uniform_prob": 1.0 / n_items,
        "top_bitstring": top_key,
        "top_key": int(top_key, 2) if top_key is not None else None,
        "found": int(top_key, 2) == int(marked) if top_key is not None else False,
    }


def teleport_circuit():
    """Teleport qubit 0 onto qubit 2. Extracted from ``3_secure_grid_link.ipynb``.

    Corrections are gates, not ``if_test``. Undoing the sent state on qubit 2
    leaves |0> when the link works. Qiskit prints qubit 2 as the left-most bit.
    """
    qc = QuantumCircuit(3, 3)
    qc.ry(1.0, 0)
    qc.rz(0.7, 0)
    qc.h(1)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.h(0)
    qc.cx(1, 2)
    qc.cz(0, 2)
    qc.rz(-0.7, 2)
    qc.ry(-1.0, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc


def analyze_teleport(counts):
    total = sum(int(v) for v in counts.values()) or 1
    q2_zero = sum(int(c) for bits, c in counts.items() if str(bits).replace(" ", "").zfill(3)[0] == "0")
    margins = []
    for index, qubit in ((2, 0), (1, 1), (0, 2)):
        zeros = sum(
            int(c)
            for bits, c in counts.items()
            if str(bits).replace(" ", "").zfill(3)[index] == "0"
        )
        margins.append({"qubit": qubit, "prob_zero": zeros / total})
    return {
        "shots": total,
        "q2_zero": q2_zero,
        "q2_zero_frac": q2_zero / total,
        "margins": margins,
        "link_works": (q2_zero / total) >= 0.9,
    }


# Four stand-in links. Costs are equal so the budget buys exactly two.
# Values follow the notebook's idea: backbone and control-center links first.
QAOA_LINKS = (
    {"id": "cc-sub-a", "value": 40.0, "cost": 10.0},
    {"id": "cc-gen", "value": 30.0, "cost": 10.0},
    {"id": "spoke-1", "value": 12.0, "cost": 10.0},
    {"id": "ring-1", "value": 8.0, "cost": 10.0},
)
QAOA_BUDGET = 20.0


def _score(chosen):
    by_id = {c["id"]: c for c in QAOA_LINKS}
    ids = [i for i in chosen if i in by_id]
    return {
        "links": ids,
        "value": float(sum(by_id[i]["value"] for i in ids)),
        "cost": float(sum(by_id[i]["cost"] for i in ids)),
        "n": len(ids),
    }


def greedy_links(budget=QAOA_BUDGET):
    order = sorted(QAOA_LINKS, key=lambda c: c["value"] / c["cost"], reverse=True)
    chosen, spent = [], 0.0
    for link in order:
        if spent + link["cost"] <= budget + 1e-9:
            chosen.append(link["id"])
            spent += link["cost"]
    return _score(chosen) | {"method": "greedy"}


def exact_links(budget=QAOA_BUDGET):
    best = {"links": [], "value": -1.0, "cost": 0.0, "n": 0}
    n = len(QAOA_LINKS)
    for mask in range(1 << n):
        cost = value = 0.0
        picks = []
        for i in range(n):
            if mask & (1 << i):
                cost += QAOA_LINKS[i]["cost"]
                if cost > budget + 1e-9:
                    break
                value += QAOA_LINKS[i]["value"]
                picks.append(QAOA_LINKS[i]["id"])
        else:
            if value > best["value"] or (value == best["value"] and cost < best["cost"]):
                best = {"links": picks, "value": value, "cost": cost, "n": len(picks)}
    return best | {"method": "exact"}


def qubo_matrices(budget=QAOA_BUDGET):
    """QUBO from notebook 6: reward value, penalize going over the budget."""
    values = np.array([c["value"] for c in QAOA_LINKS], float)
    costs = np.array([c["cost"] for c in QAOA_LINKS], float)
    penalty = (values.max() + 5.0) / (costs.min() ** 2) * 20.0
    linear = -values + penalty * (costs**2 - 2.0 * budget * costs)
    quad = np.zeros((len(QAOA_LINKS), len(QAOA_LINKS)))
    for i in range(len(QAOA_LINKS)):
        for j in range(i + 1, len(QAOA_LINKS)):
            quad[i, j] = quad[j, i] = 2.0 * penalty * costs[i] * costs[j]
    return linear, quad, float(penalty)


def qaoa_circuit(params, linear, quad, p=1):
    """One QAOA layer. Phase separator is RZ / RZZ, mixer is RX. From notebook 6."""
    gammas, betas = params[:p], params[p:]
    n = len(linear)
    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    for layer in range(p):
        g = float(gammas[layer])
        for i in range(n):
            if abs(linear[i]) > 1e-12:
                qc.rz(2 * g * linear[i], i)
        for i in range(n):
            for j in range(i + 1, n):
                if abs(quad[i, j]) > 1e-12:
                    qc.cx(i, j)
                    qc.rz(2 * g * quad[i, j], j)
                    qc.cx(i, j)
        for q in range(n):
            qc.rx(2 * float(betas[layer]), q)
    qc.measure(range(n), range(n))
    return qc


def _energy(bits, linear, quad):
    x = np.asarray(bits, dtype=float)
    return float(linear @ x + 0.5 * x @ quad @ x)


def _counts_energy(counts, linear, quad):
    total = sum(counts.values())
    acc = 0.0
    n = len(linear)
    for bitstring, c in counts.items():
        bits = [int(b) for b in str(bitstring).replace(" ", "").zfill(n)[::-1]]
        acc += _energy(bits, linear, quad) * int(c)
    return acc / total


def optimize_qaoa(shots=256, seed=7):
    """Grid-search one QAOA layer on Aer, then keep the lowest-energy angles."""
    linear, quad, penalty = qubo_matrices()
    sim = AerSimulator()
    best = None
    gammas = np.linspace(0.05, 1.0, 5)
    betas = np.linspace(0.15, np.pi / 2, 5)
    evaluated = 0
    for gamma in gammas:
        for beta in betas:
            qc = qaoa_circuit(np.array([gamma, beta]), linear, quad, p=1)
            counts = sim.run(transpile(qc, sim), shots=shots, seed_simulator=seed).result().get_counts()
            energy = _counts_energy(counts, linear, quad)
            evaluated += 1
            if best is None or energy < best["energy"]:
                best = {"energy": energy, "gamma": float(gamma), "beta": float(beta)}
    params = np.array([best["gamma"], best["beta"]])
    circuit = qaoa_circuit(params, linear, quad, p=1)
    return circuit, {
        "p": 1,
        "gamma": best["gamma"],
        "beta": best["beta"],
        "train_energy": best["energy"],
        "train_shots": shots,
        "evaluated": evaluated,
        "penalty": penalty,
        "budget": QAOA_BUDGET,
        "links": [dict(link) for link in QAOA_LINKS],
    }


def analyze_qaoa(counts, budget=QAOA_BUDGET):
    """Best feasible bitstring in the sample, next to greedy and exact."""
    exact = exact_links(budget)
    greedy = greedy_links(budget)
    n = len(QAOA_LINKS)
    total = sum(int(v) for v in counts.values()) or 1
    best = None
    top = None
    for bitstring, c in sorted(counts.items(), key=lambda kv: -int(kv[1])):
        raw = str(bitstring).replace(" ", "").zfill(n)
        bits = [int(b) for b in raw[::-1]]
        ids = [QAOA_LINKS[i]["id"] for i in range(n) if bits[i]]
        scored = _score(ids) | {"bitstring": raw, "prob": int(c) / total}
        if top is None:
            top = scored
        if scored["cost"] <= budget + 1e-9:
            if best is None or scored["value"] > best["value"]:
                best = scored
    # Qubit i is QAOA_LINKS[i]. Qiskit prints qubit n-1 on the left.
    exact_qiskit = "".join(
        "1" if QAOA_LINKS[i]["id"] in set(exact["links"]) else "0" for i in range(n - 1, -1, -1)
    )
    optimal_hits = sum(int(c) for bits, c in counts.items() if str(bits).replace(" ", "").zfill(n) == exact_qiskit)
    return {
        "exact": exact,
        "greedy": greedy,
        "qaoa_best_feasible": best,
        "qaoa_most_frequent": top,
        "matches_exact": bool(best and set(best["links"]) == set(exact["links"])),
        "optimal_prob": optimal_hits / total,
        "shots": total,
        "optimal_bitstring": exact_qiskit,
    }


def aer_counts(circuit, shots, seed=1):
    sim = AerSimulator()
    compiled = transpile(circuit, sim)
    result = sim.run(compiled, shots=shots, seed_simulator=seed).result()
    return {str(k): int(v) for k, v in result.get_counts().items()}


# Gates the qBraid QIR and IonQ converters accept. Custom names such as "QFT†"
# and Qiskit's ``u`` gate are flattened before a job is submitted.
_SUBMIT_BASIS = (
    "ccx",
    "cx",
    "cz",
    "h",
    "id",
    "rx",
    "ry",
    "rz",
    "s",
    "sdg",
    "swap",
    "t",
    "tdg",
    "x",
    "y",
    "z",
)


def for_submission(circuit):
    """Return an OpenQASM 3 program with only gates the qBraid converters accept."""
    from qiskit import qasm3

    flat = transpile(circuit.decompose(reps=12), basis_gates=list(_SUBMIT_BASIS), optimization_level=1)
    return qasm3.dumps(flat)
