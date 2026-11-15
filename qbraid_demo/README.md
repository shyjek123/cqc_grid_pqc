# Secure-grid qBraid demo

Circuits extracted from `src`: BB84, Shor's factoring of 15, Grover search, teleportation, and a four-link QAOA selection (notebook 6's circuit, small enough for a free simulator).

`run_demo.py` runs them on local Qiskit Aer, then follows qBraid's agent loop:

1. List devices with `QbraidProvider`.
2. Quote every cloud job with `estimate_cost` before submission.
3. Submit the free simulators `qbraid:qbraid:sim:qir-sv`, `ionq:ionq:sim:simulator`, and `quantinuum:quantinuum:sim:h2-emulator` only when that quote is 0 credits. Those jobs share one `GroupJobSession`.
4. Submit a gate-model QPU only when the quote is within the credit ceiling and the account balance covers it. Analog QPUs and `openquantum:` devices are skipped. Emulators are labeled as emulators.

The API key is read from `~/.qbraid/qbraidrc` by the qBraid SDK. It is not stored in this directory.

## Run

From this directory, with the project virtualenv:

```bash
/home/bastek/projects/citadel/research/pqc/hackathon/.venv/bin/python run_demo.py
```

Figures land in `results/figures/`. The write-up is `results/ANALYSIS.md`, with `results/evidence.json` and `results/runs.csv`.

## Credit ceiling

```bash
export QBRAID_MAX_CREDITS=100   # default; a QPU quote above this is not submitted
export QBRAID_RUN_HARDWARE=1    # set to 0 to quote hardware and skip submission
export QBRAID_WAIT_SECONDS=300  # how long to poll before recording a still-queued job id
```

`QBRAID_MAX_CREDITS` is also capped by the live credit balance. A missing balance skips hardware.
