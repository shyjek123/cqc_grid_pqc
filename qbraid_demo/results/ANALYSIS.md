# Secure-grid demo results

Generated 2026-11-15 03:58:13 UTC.

Programs come from the notebooks in `src`: BB84, Shor's factoring of 15, Grover search, teleportation, and the QAOA link-selection circuit. The agent runs them on local Aer, quotes qBraid, submits free simulators only when `estimate_cost` returns 0 credits, and submits a gate-model QPU only when the quote fits the credit ceiling and the balance.

Emulator results are emulator results. They are not QPU results. A QPU error rate here is the processor's error on this circuit, not the error rate of a utility fiber.

## Steps

- 2026-11-15 03:42:23 UTC: Start the secure-grid qBraid demo.
- 2026-11-15 03:42:23 UTC: Build the circuits from src/ and run them on Qiskit Aer.
- 2026-11-15 03:42:25 UTC: Aer BB84 QBER is 0.000 with no spy and 0.235 when Eve resends every qubit.
- 2026-11-15 03:42:25 UTC: Aer Shor returned period 4 and factors [3, 5].
- 2026-11-15 03:42:26 UTC: Listed 43 qBraid devices, 26 online.
- 2026-11-15 03:42:26 UTC: Account balance is 5500.00 credits.
- 2026-11-15 03:42:27 UTC: Submit 10 free-simulator job(s) in one group.
- 2026-11-15 03:42:28 UTC: Submitted bb84 to qbraid:qbraid:sim:qir-sv: qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a24c8f5265fb3f23cf4
- 2026-11-15 03:42:29 UTC: Submitted grover to qbraid:qbraid:sim:qir-sv: qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a24c8f5265fb3f23cf7
- 2026-11-15 03:42:29 UTC: Submitted teleport to qbraid:qbraid:sim:qir-sv: qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a25c8f5265fb3f23cfb
- 2026-11-15 03:42:42 UTC: Submitted shor to qbraid:qbraid:sim:qir-sv: qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a32c8f5265fb3f23d02
- 2026-11-15 03:42:43 UTC: Submitted qaoa to qbraid:qbraid:sim:qir-sv: qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a33c8f5265fb3f23d05
- 2026-11-15 03:42:44 UTC: Submitted bb84 to ionq:ionq:sim:simulator: ionq:ionq:sim:simulator-d708-qjob-6af92a34c8f5265fb3f23d0a
- 2026-11-15 03:42:45 UTC: Submitted grover to ionq:ionq:sim:simulator: ionq:ionq:sim:simulator-d708-qjob-6af92a35c8f5265fb3f23d0f
- 2026-11-15 03:42:46 UTC: Submitted teleport to ionq:ionq:sim:simulator: ionq:ionq:sim:simulator-d708-qjob-6af92a35c8f5265fb3f23d16
- 2026-11-15 03:42:46 UTC: Refused grover on quantinuum:quantinuum:sim:h2-emulator: ProgramConversionError: Failed to convert 'qasm3' to 'qasm2' due to the following error(s):

Conversion qasm3 -> qiskit -> qasm2 failed due to exception raised while converting from 'qasm3'.
MissingOptionalLibraryError: "The 'qiskit_qasm3_import' library is required to use 'loading from OpenQASM 3'. You can install it with 'pip install qiskit_qasm3_import'."

- 2026-11-15 03:42:46 UTC: Refused teleport on quantinuum:quantinuum:sim:h2-emulator: ProgramConversionError: Failed to convert 'qasm3' to 'qasm2' due to the following error(s):

Conversion qasm3 -> qiskit -> qasm2 failed due to exception raised while converting from 'qasm3'.
MissingOptionalLibraryError: "The 'qiskit_qasm3_import' library is required to use 'loading from OpenQASM 3'. You can install it with 'pip install qiskit_qasm3_import'."

- 2026-11-15 03:42:49 UTC: Hardware plan: 7 QPU jobs, quoted 5455.50 credits, ceiling 5500.00.
- 2026-11-15 03:42:50 UTC: Launched qBraid codeq agent secure-grid-qpu-034249 to submit the hardware plan.
- 2026-11-15 03:43:04 UTC: Submitted bb84 to rigetti:rigetti:qpu:cepheus-1-108q (500 shots, quote 24.2 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3bc8f5265fb3f23d1e
- 2026-11-15 03:43:04 UTC: Submitted shor to rigetti:rigetti:qpu:cepheus-1-108q (256 shots, quote 14.3424 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3dc8f5265fb3f23d21
- 2026-11-15 03:43:04 UTC: Submitted qaoa to rigetti:rigetti:qpu:cepheus-1-108q (400 shots, quote 20.16 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3fc8f5265fb3f23d24
- 2026-11-15 03:43:04 UTC: Submitted teleport to rigetti:rigetti:qpu:cepheus-1-108q (1000 shots, quote 44.4 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a41c8f5265fb3f23d28
- 2026-11-15 03:43:04 UTC: Submitted grover to rigetti:rigetti:qpu:cepheus-1-108q (1000 shots, quote 44.4 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a43c8f5265fb3f23d2b
- 2026-11-15 03:43:04 UTC: Submitted shor to aws:ionq:qpu:forte-1 (256 shots, quote 2078.0 credits): aws:ionq:qpu:forte-1-d708-qjob-6af92a46c8f5265fb3f23d2e
- 2026-11-15 03:43:04 UTC: Not submitted: qaoa on aws:ionq:qpu:forte-1.
- 2026-11-15 03:43:04 UTC: Poll jobs for up to 900s.
- 2026-11-15 03:43:08 UTC: Waiting on 8 job(s): bb84@simulator, grover@simulator, bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q, shor@forte-1
- 2026-11-15 03:43:17 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:43:25 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:43:34 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:43:42 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:43:50 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:43:59 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:44:07 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:44:16 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:44:24 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:44:33 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:44:41 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:44:50 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:44:58 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:45:06 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:45:15 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:45:24 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:45:32 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:45:40 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:45:49 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:45:58 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:46:06 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:46:14 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:46:23 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:46:31 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:46:40 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:46:49 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:46:57 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:47:05 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:47:14 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:47:22 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:47:31 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:47:39 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:47:48 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:47:56 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:48:04 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:48:13 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:48:21 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:48:30 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:48:38 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:48:47 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:48:55 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:49:03 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:49:12 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:49:20 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:49:29 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:49:37 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:49:46 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:49:54 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:50:03 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:50:11 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:50:20 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:50:28 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:50:36 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:50:45 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:50:53 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:51:02 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:51:10 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:51:19 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:51:27 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:51:35 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:51:44 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:51:52 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:52:01 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:52:09 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:52:18 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:52:26 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:52:35 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:52:43 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:52:52 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:53:01 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:53:09 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:53:17 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:53:26 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:53:34 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:53:43 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:53:51 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:54:00 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:54:08 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:54:17 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:54:25 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:54:33 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:54:42 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:54:50 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:54:59 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:55:07 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:55:15 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:55:24 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:55:32 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:55:41 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:55:49 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:55:57 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:56:06 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:56:14 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:56:23 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:56:31 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:56:40 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:56:48 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:56:56 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:57:05 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:57:13 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:57:22 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:57:30 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:57:38 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:57:47 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:57:55 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:58:04 UTC: Waiting on 5 job(s): bb84@cepheus-1-108q, shor@cepheus-1-108q, qaoa@cepheus-1-108q, teleport@cepheus-1-108q, grover@cepheus-1-108q
- 2026-11-15 03:58:12 UTC: Cloud collection finished with counts from 8 job(s).
- 2026-11-15 03:58:12 UTC: Draw the figures and write the analysis from the counts that came back.

## BB84

Each point is 200 qubits on the local Aer simulator. Eve measures that fraction in a random basis and resends. The error rate is only on rounds where Alice and Bob picked the same basis. The gray line in the figure is 0.25 times Eve's fraction, the usual intercept-resend average.

| Eve fraction | Sifted bits | Errors | QBER |
|---:|---:|---:|---:|
| 0.0 | 93 | 0 | 0.000 |
| 0.1 | 98 | 3 | 0.031 |
| 0.2 | 114 | 5 | 0.044 |
| 0.3 | 107 | 5 | 0.047 |
| 0.4 | 110 | 9 | 0.082 |
| 0.5 | 92 | 11 | 0.120 |
| 0.6 | 86 | 13 | 0.151 |
| 0.7 | 102 | 20 | 0.196 |
| 0.8 | 96 | 16 | 0.167 |
| 0.9 | 102 | 22 | 0.216 |
| 1.0 | 85 | 20 | 0.235 |

With no spy the sifted error rate was 0.000 (0 errors in 93 sifted bits). With Eve on every qubit it was 0.235 (20 of 85).
In this sample the error rate first reached the 11% one-way security bound at Eve fraction 0.5 (QBER 0.120). That 11% line is the Shor–Preskill one-way bound, not a field alarm setting.

A second circuit puts clean rounds and an in-circuit spy on one chip so the same program can be sent to a simulator or a QPU. On Aer (200 shots, 16 qubits) the clean-round error rate was 0.000 and the spy-round error rate was 0.233.

| Backend | Kind | Clean error | Spy error | Shots | Job |
|---|---|---:|---:|---:|---|
| Aer | simulator | 0.000 | 0.233 | 200 | local |
| `qbraid:qbraid:sim:qir-sv` | simulator | 0.000 | 0.256 | 200 | `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a24c8f5265fb3f23cf4` |
| `ionq:ionq:sim:simulator` | simulator | 0.000 | 0.210 | 200 | `ionq:ionq:sim:simulator-d708-qjob-6af92a34c8f5265fb3f23d0a` |

## Shor, factoring 15

The local run used 4 counting qubits and 1024 shots. The multiply-by-7-mod-15 step is the notebook's hand-built gate. It does not factor a general RSA modulus. The notebook's longer register is 8 counting qubits; 4 counting qubits already resolve the period 4.

Accepted period: 4. Factors of 15 from that period: 3 and 5.

| Bitstring | Counts | Phase | Candidate period | 7^r mod 15 | Used |
|---|---:|---:|---:|---:|---|
| `0000` | 277 | 0.0000 | 1 | 7 | no |
| `1100` | 255 | 0.7500 | 4 | 1 | yes |
| `0100` | 253 | 0.2500 | 4 | 1 | no |
| `1000` | 239 | 0.5000 | 2 | 4 | no |

`qbraid:qbraid:sim:qir-sv` (simulator, job `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a32c8f5265fb3f23d02`, 256 shots) accepted period 4 and factors 3 and 5.

## Grover

Aer, N = 4: marked key 2, 1 iteration(s), 1024 shots. Success probability 100.0% against a uniform 25.0%. Most common key 2 (the marked key).

Aer, N = 8: marked key 5, 2 iteration(s), 1024 shots. Success probability 93.6% against a uniform 12.5%. Most common key 5 (the marked key).

| Backend | Kind | Success | Shots | Top key | Job |
|---|---|---:|---:|---:|---|
| Aer | simulator | 100.0% | 1024 | 2 | local |
| `qbraid:qbraid:sim:qir-sv` | simulator | 100.0% | 200 | 2 | `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a24c8f5265fb3f23cf7` |
| `ionq:ionq:sim:simulator` | simulator | 100.0% | 200 | 2 | `ionq:ionq:sim:simulator-d708-qjob-6af92a35c8f5265fb3f23d0f` |

## Teleportation link

The circuit is the notebook's three-qubit teleport. Corrections are gates. Undoing the prepared state on qubit 2 should leave |0>, which is the left-most bit in Qiskit's print order.

Aer: qubit 2 read 0 on 1024 of 1024 shots (100.0%).

Aer marginals: qubit 0 was 0 on 47.8% of shots, qubit 1 was 0 on 50.0% of shots, qubit 2 was 0 on 100.0% of shots. Qubits 0 and 1 are the Bell measurement and should stay mixed.

| Backend | Kind | Qubit 2 = 0 | Shots | Job |
|---|---|---:|---:|---|
| Aer | simulator | 100.0% | 1024 | local |
| `qbraid:qbraid:sim:qir-sv` | simulator | 100.0% | 200 | `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a25c8f5265fb3f23cfb` |
| `ionq:ionq:sim:simulator` | simulator | 94.5% | 200 | `ionq:ionq:sim:simulator-d708-qjob-6af92a35c8f5265fb3f23d16` |

## QKD link selection

Notebook 6 compares greedy, exact search, and one QAOA layer. This run uses four links with equal cost 10 and a budget of 20, so the exact answer is the two highest-value links. The 16-link city instance stays in the notebook; four qubits fit a free simulator and a small QPU.

Greedy value 70.0 on cc-sub-a, cc-gen.
Exact value 70.0 on cc-sub-a, cc-gen.
Best feasible QAOA sample value 70.0 on cc-sub-a, cc-gen (probability of that bitstring 28.5%). It matches the exact set. Probability of the exact bitstring `0011` was 28.5% in 1024 Aer shots. Training used gamma 0.050 and beta 0.860.

`qbraid:qbraid:sim:qir-sv` (simulator, job `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a33c8f5265fb3f23d05`, 400 shots) best feasible value 70.0 on cc-sub-a, cc-gen; exact-bitstring probability 27.8%.

## Devices, quotes, and jobs

codeq did not start. Submitting the same plan with qbraid jobs submit. CLI refused qaoa on aws:ionq:qpu:forte-1: aid credits. Required: 3230.00, Available: 2994.22.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/bastek/.local/share/mise/installs/python/3.14.6/lib/python3.14/site-packages/qbraid_cli/jobs/app.py", line 277, in jobs_submit
    job = run_progress_task(submit_job, description="Submitting job...")
  File "/home/bastek/.local/share/mise/installs/python/3.14.6/lib/python3.14/site-packages/qbraid_cli/handlers.py", line 205, in run_progress_task
    return handle_error(message=custom_message, include_traceback=include_error_traceback)
  File "/home/bastek/.local/share/mise/installs/python/3.14.6/lib/python3.14/site-packages/qbraid_cli/handlers.py", line 69, in handle_error
    raise typer.Exit(code=1)
typer.exceptions.Exit Submitted bb84 to rigetti:rigetti:qpu:cepheus-1-108q (500 shots, quote 24.2 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3bc8f5265fb3f23d1e Submitted shor to rigetti:rigetti:qpu:cepheus-1-108q (256 shots, quote 14.3424 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3dc8f5265fb3f23d21 Submitted qaoa to rigetti:rigetti:qpu:cepheus-1-108q (400 shots, quote 20.16 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3fc8f5265fb3f23d24 Submitted teleport to rigetti:rigetti:qpu:cepheus-1-108q (1000 shots, quote 44.4 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a41c8f5265fb3f23d28 Submitted grover to rigetti:rigetti:qpu:cepheus-1-108q (1000 shots, quote 44.4 credits): rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a43c8f5265fb3f23d2b Submitted shor to aws:ionq:qpu:forte-1 (256 shots, quote 2078.0 credits): aws:ionq:qpu:forte-1-d708-qjob-6af92a46c8f5265fb3f23d2e Not submitted: qaoa on aws:ionq:qpu:forte-1.

Credit balance read for this run: 5500.00. Ceiling: 5500.0 credits.

Free-simulator group: `group:d708-6af92a23a807fbc4243e3003`.

The account listed 43 devices, 26 online, 12 of them online gate-model QPUs.
Largest online gate-model QPU in this listing: Boston (`ibm:ibm:qpu:boston`), 156 qubits.

| Online gate QPU | Qubits | Queue |
|---|---:|---:|
| `ibm:ibm:qpu:boston` | 156 | 1 |
| `ibm:ibm:qpu:kingston` | 156 | 223 |
| `ibm:ibm:qpu:marrakesh` | 156 | 1 |
| `ibm:ibm:qpu:miami` | 120 | 0 |
| `openquantum:rigetti:qpu:cepheus-1-108q` | 107 | None |
| `rigetti:rigetti:qpu:cepheus-1-108q` | 107 | None |
| `openquantum:iqm:qpu:emerald` | 54 | None |
| `aws:ionq:qpu:forte-1` | 36 | 0 |
| `openquantum:ionq:qpu:forte-1` | 36 | None |
| `openquantum:ionq:qpu:forte-enterprise` | 36 | None |
| `openquantum:iqm:qpu:garnet` | 20 | None |
| `openquantum:aqt:qpu:ibex-q1` | 12 | None |

Hardware quotes from `estimate_cost`, before any QPU submission:

| Device | Shots | Quote (credits) | Priced |
|---|---:|---:|---|
| `ibm:ibm:qpu:marrakesh` (bb84) | 500 | — | no |
| `ibm:ibm:qpu:marrakesh` (shor) | 256 | — | no |
| `ibm:ibm:qpu:marrakesh` (qaoa) | 400 | — | no |
| `ibm:ibm:qpu:marrakesh` (teleport) | 1000 | — | no |
| `ibm:ibm:qpu:marrakesh` (grover) | 1000 | — | no |
| `ibm:ibm:qpu:kingston` (bb84) | 500 | — | no |
| `ibm:ibm:qpu:kingston` (shor) | 256 | — | no |
| `ibm:ibm:qpu:kingston` (qaoa) | 400 | — | no |
| `ibm:ibm:qpu:kingston` (teleport) | 1000 | — | no |
| `ibm:ibm:qpu:kingston` (grover) | 1000 | — | no |
| `ibm:ibm:qpu:miami` (bb84) | 500 | — | no |
| `ibm:ibm:qpu:miami` (shor) | 256 | — | no |
| `ibm:ibm:qpu:miami` (qaoa) | 400 | — | no |
| `ibm:ibm:qpu:miami` (teleport) | 1000 | — | no |
| `ibm:ibm:qpu:miami` (grover) | 1000 | — | no |
| `aws:ionq:qpu:forte-1` (bb84) | 500 | 4030 | yes |
| `aws:ionq:qpu:forte-1` (shor) | 256 | 2078 | yes |
| `aws:ionq:qpu:forte-1` (qaoa) | 400 | 3230 | yes |
| `aws:ionq:qpu:forte-1` (teleport) | 1000 | 8030 | yes |
| `aws:ionq:qpu:forte-1` (grover) | 1000 | 8030 | yes |
| `ibm:ibm:qpu:boston` (bb84) | 500 | — | no |
| `ibm:ibm:qpu:boston` (shor) | 256 | — | no |
| `ibm:ibm:qpu:boston` (qaoa) | 400 | — | no |
| `ibm:ibm:qpu:boston` (teleport) | 1000 | — | no |
| `ibm:ibm:qpu:boston` (grover) | 1000 | — | no |
| `rigetti:rigetti:qpu:cepheus-1-108q` (bb84) | 500 | 24.2 | yes |
| `rigetti:rigetti:qpu:cepheus-1-108q` (shor) | 256 | 14.3424 | yes |
| `rigetti:rigetti:qpu:cepheus-1-108q` (qaoa) | 400 | 20.16 | yes |
| `rigetti:rigetti:qpu:cepheus-1-108q` (teleport) | 1000 | 44.4 | yes |
| `rigetti:rigetti:qpu:cepheus-1-108q` (grover) | 1000 | 44.4 | yes |

| Experiment | Kind | Device | Shots | Quote | Status | Job |
|---|---|---|---:|---:|---|---|
| grover | emulator | `quantinuum:quantinuum:sim:h2-emulator` | 200 | 0 | REFUSED ProgramConversionError: Failed to convert 'qasm3' to 'qasm2' due to the following error(s):

Conversion qasm3 -> qiskit -> qasm2 failed due to exception raised while converting from 'qasm3'.
MissingOptionalLibraryError: "The 'qiskit_qasm3_import' library is required to use 'loading from OpenQASM 3'. You can install it with 'pip install qiskit_qasm3_import'."
 | `` |
| teleport | emulator | `quantinuum:quantinuum:sim:h2-emulator` | 200 | 0 | REFUSED ProgramConversionError: Failed to convert 'qasm3' to 'qasm2' due to the following error(s):

Conversion qasm3 -> qiskit -> qasm2 failed due to exception raised while converting from 'qasm3'.
MissingOptionalLibraryError: "The 'qiskit_qasm3_import' library is required to use 'loading from OpenQASM 3'. You can install it with 'pip install qiskit_qasm3_import'."
 | `` |
| bb84 | simulator | `qbraid:qbraid:sim:qir-sv` | 200 | 0 | COMPLETED | `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a24c8f5265fb3f23cf4` |
| grover | simulator | `qbraid:qbraid:sim:qir-sv` | 200 | 0 | COMPLETED | `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a24c8f5265fb3f23cf7` |
| teleport | simulator | `qbraid:qbraid:sim:qir-sv` | 200 | 0 | COMPLETED | `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a25c8f5265fb3f23cfb` |
| shor | simulator | `qbraid:qbraid:sim:qir-sv` | 256 | 0 | COMPLETED | `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a32c8f5265fb3f23d02` |
| qaoa | simulator | `qbraid:qbraid:sim:qir-sv` | 400 | 0 | COMPLETED | `qbraid:qbraid:sim:qir-sv-d708-qjob-6af92a33c8f5265fb3f23d05` |
| teleport | simulator | `ionq:ionq:sim:simulator` | 200 | 0 | COMPLETED noise `aria-1` | `ionq:ionq:sim:simulator-d708-qjob-6af92a35c8f5265fb3f23d16` |
| bb84 | simulator | `ionq:ionq:sim:simulator` | 200 | 0 | COMPLETED noise `aria-1` | `ionq:ionq:sim:simulator-d708-qjob-6af92a34c8f5265fb3f23d0a` |
| grover | simulator | `ionq:ionq:sim:simulator` | 200 | 0 | COMPLETED noise `aria-1` | `ionq:ionq:sim:simulator-d708-qjob-6af92a35c8f5265fb3f23d0f` |
| shor | qpu | `aws:ionq:qpu:forte-1` | 256 | 2078 | FAILED | `aws:ionq:qpu:forte-1-d708-qjob-6af92a46c8f5265fb3f23d2e` |
| bb84 | qpu | `rigetti:rigetti:qpu:cepheus-1-108q` | 500 | 24.2 | QUEUED still QUEUED after 900s | `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3bc8f5265fb3f23d1e` |
| shor | qpu | `rigetti:rigetti:qpu:cepheus-1-108q` | 256 | 14.3424 | QUEUED still QUEUED after 900s | `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3dc8f5265fb3f23d21` |
| qaoa | qpu | `rigetti:rigetti:qpu:cepheus-1-108q` | 400 | 20.16 | QUEUED still QUEUED after 900s | `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3fc8f5265fb3f23d24` |
| teleport | qpu | `rigetti:rigetti:qpu:cepheus-1-108q` | 1000 | 44.4 | QUEUED still QUEUED after 900s | `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a41c8f5265fb3f23d28` |
| grover | qpu | `rigetti:rigetti:qpu:cepheus-1-108q` | 1000 | 44.4 | QUEUED still QUEUED after 900s | `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a43c8f5265fb3f23d2b` |

Hardware job `aws:ionq:qpu:forte-1-d708-qjob-6af92a46c8f5265fb3f23d2e` on `aws:ionq:qpu:forte-1` was still FAILED when polling stopped. No counts from that job are included above.
Hardware job `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3bc8f5265fb3f23d1e` on `rigetti:rigetti:qpu:cepheus-1-108q` was still QUEUED when polling stopped. No counts from that job are included above.
Hardware job `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3dc8f5265fb3f23d21` on `rigetti:rigetti:qpu:cepheus-1-108q` was still QUEUED when polling stopped. No counts from that job are included above.
Hardware job `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a3fc8f5265fb3f23d24` on `rigetti:rigetti:qpu:cepheus-1-108q` was still QUEUED when polling stopped. No counts from that job are included above.
Hardware job `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a41c8f5265fb3f23d28` on `rigetti:rigetti:qpu:cepheus-1-108q` was still QUEUED when polling stopped. No counts from that job are included above.
Hardware job `rigetti:rigetti:qpu:cepheus-1-108q-d708-qjob-6af92a43c8f5265fb3f23d2b` on `rigetti:rigetti:qpu:cepheus-1-108q` was still QUEUED when polling stopped. No counts from that job are included above.

## Figures

- bb84_sweep: `/home/bastek/projects/citadel/research/pqc/hackathon/qhackathon_secure_grid/qbraid_demo/results/figures/bb84_qber_sweep.png`
- bb84_backends: `/home/bastek/projects/citadel/research/pqc/hackathon/qhackathon_secure_grid/qbraid_demo/results/figures/bb84_clean_vs_spy.png`
- grover: `/home/bastek/projects/citadel/research/pqc/hackathon/qhackathon_secure_grid/qbraid_demo/results/figures/grover_search.png`
- shor: `/home/bastek/projects/citadel/research/pqc/hackathon/qhackathon_secure_grid/qbraid_demo/results/figures/shor_phases.png`
- teleport: `/home/bastek/projects/citadel/research/pqc/hackathon/qhackathon_secure_grid/qbraid_demo/results/figures/teleport_link.png`
- qaoa: `/home/bastek/projects/citadel/research/pqc/hackathon/qhackathon_secure_grid/qbraid_demo/results/figures/qaoa_link_selection.png`
- overview: `/home/bastek/projects/citadel/research/pqc/hackathon/qhackathon_secure_grid/qbraid_demo/results/figures/results_overview.png`
- qpu_gap: `/home/bastek/projects/citadel/research/pqc/hackathon/qhackathon_secure_grid/qbraid_demo/results/figures/gate_qpu_qubits.png`

## What this run does not show

BB84 here is a circuit experiment, not a fiber QKD link. The notebook does not do error correction or privacy amplification, and neither does this demo. Shor's gate is hardcoded for 15. Grover's oracle is the known key, not AES. The QAOA instance is four links, not the city network in notebook 6.
