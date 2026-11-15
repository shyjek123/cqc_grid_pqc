# Secure-grid qBraid demo

Circuits extracted from `src`: BB84, Shor's factoring of 15, Grover search, teleportation, and a four-link QAOA selection (notebook 6's circuit, small enough for a free simulator).

`run_demo.py` runs them on local Qiskit Aer, then follows qBraid's agent loop:

1. List devices with `QbraidProvider`.
2. Quote every cloud job with `estimate_cost` before submission.
3. Submit the free simulators `qbraid:qbraid:sim:qir-sv`, `ionq:ionq:sim:simulator`, and `quantinuum:quantinuum:sim:h2-emulator` only when that quote is 0 credits. Those jobs share one `GroupJobSession`.
4. Quote every online gate-model QPU. Analog QPUs and `openquantum:` devices are skipped. The plan keeps every job whose quote still fits the credit ceiling, one circuit per device, until the ceiling is used. Emulators are labeled as emulators.
5. Launch a qBraid `codeq` agent in this terminal (`qbraid agents launch -t codeq --approval auto`). The agent submits only the commands in `results/agent_task.md`, each one a `qbraid jobs submit` of the OpenQASM written under `results/programs/`.

The API key is read from `~/.qbraid/qbraidrc`. It is not stored in this directory.

## Run on real hardware

From this directory, with the project virtualenv. This spends credits, up to 5500 or your balance, whichever is smaller.

```bash
/home/bastek/projects/citadel/research/pqc/hackathon/.venv/bin/python run_demo.py \
  --max-credits 5500 \
  --wait-seconds 900 \
  --agent-seconds 240
```

The same defaults apply with no flags. Figures land in `results/figures/`. The write-up is `results/ANALYSIS.md`, with `results/evidence.json`, `results/runs.csv`, and `results/hardware_plan.json`.

`--no-hardware` skips QPUs. `--local-only` stays on Aer. `--cli-submit` skips the agent and runs `qbraid jobs submit` from this process. Use that only after the agent has stopped, or the same circuits can be billed twice.

```bash
export QBRAID_MAX_CREDITS=5500
export QBRAID_RUN_HARDWARE=1
export QBRAID_USE_AGENT=1
export QBRAID_AGENT_SECONDS=240
export QBRAID_WAIT_SECONDS=900
```
