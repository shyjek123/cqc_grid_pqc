Submit the qBraid hardware jobs below. Use only `qbraid jobs submit`.
The quoted total is 5455.5024 credits. Stop before exceeding 5500.0000 credits.
Do not add devices, shots, or circuits. Do not submit a row twice.
After each command, append one JSON object to results/agent_jobs.jsonl with keys
name, device, experiment, job_id (the jobQrn), and estimated_credits.
When every row has been submitted, print a line that is exactly: AGENT_DONE

qbraid jobs submit results/programs/bb84.qasm -d rigetti:rigetti:qpu:cepheus-1-108q -f qasm3 --shots 500 --name grid-bb84-1 --tags '{"demo": "secure-grid", "experiment": "bb84", "hardware": true}' --json
qbraid jobs submit results/programs/shor.qasm -d rigetti:rigetti:qpu:cepheus-1-108q -f qasm3 --shots 256 --name grid-shor-2 --tags '{"demo": "secure-grid", "experiment": "shor", "hardware": true}' --json
qbraid jobs submit results/programs/qaoa.qasm -d rigetti:rigetti:qpu:cepheus-1-108q -f qasm3 --shots 400 --name grid-qaoa-3 --tags '{"demo": "secure-grid", "experiment": "qaoa", "hardware": true}' --json
qbraid jobs submit results/programs/teleport.qasm -d rigetti:rigetti:qpu:cepheus-1-108q -f qasm3 --shots 1000 --name grid-teleport-4 --tags '{"demo": "secure-grid", "experiment": "teleport", "hardware": true}' --json
qbraid jobs submit results/programs/grover.qasm -d rigetti:rigetti:qpu:cepheus-1-108q -f qasm3 --shots 1000 --name grid-grover-5 --tags '{"demo": "secure-grid", "experiment": "grover", "hardware": true}' --json
qbraid jobs submit results/programs/shor.qasm -d aws:ionq:qpu:forte-1 -f qasm3 --shots 256 --name grid-shor-6 --tags '{"demo": "secure-grid", "experiment": "shor", "hardware": true}' --json
qbraid jobs submit results/programs/qaoa.qasm -d aws:ionq:qpu:forte-1 -f qasm3 --shots 400 --name grid-qaoa-7 --tags '{"demo": "secure-grid", "experiment": "qaoa", "hardware": true}' --json
