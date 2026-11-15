# Step 3: Secure Grid Backbone

## Architecture

A control center and a substation share a fiber link. The fiber carries entangled photon pairs, and an ordinary network carries two correction bits per teleported qubit. The teleported qubits become key material for AES-256.

**Trusted-node problem:** fiber loses photons over distance, so long QKD links use relay stations. Each relay sees the key, so each one must be trusted [1][2]. With teleportation, a middle station only swaps entanglement and passes on classical bits. It never holds the key [3]. This is a proposed design: repeaters like this aren't deployed yet.

## Assumptions and tradeoffs

- The classical channel must be authenticated, because teleportation and QKD don't confirm who's on the other end [1][4]. Use ML-DSA signatures or a pre-shared key.
- Post-quantum cryptography (ML-KEM, ML-DSA) is the default everywhere, because it's just software [5]. The quantum link adds a second layer only on high-value fiber.
- If the quantum link fails, traffic falls back to ML-KEM, so the grid stays online.

## The working link

Alice sends qubit 0 to Bob's qubit 2 using an entangled pair (qubits 1 and 2) [6]. To check it, the circuit undoes the sent state on qubit 2. If teleportation worked, qubit 2 reads 0.

| Run | Qubit 2 read 0 |
|---|---|
| Qiskit Aer (noise-free) | 1024 / 1024 |
| IonQ simulator, `forte-1` noise | 196 / 200 (98%) |

IonQ job ID: `ionq:ionq:sim:simulator-d6f1-qjob-6af8fbe9c8f5265fb3f21b24`

All three qubits are on one chip, so this shows how the link works, not how far it reaches.

## Rollout

1. Put ML-KEM on all control-center-to-substation links.
2. Pilot one quantum link on existing fiber to a critical substation.
3. Expand only if the pilot stays reliable and falls back cleanly.

## Cost vs. security

Post-quantum cryptography is a cheap software update and protects every link. Quantum links need dedicated hardware and fiber, so they're worth it only on a few critical links. Both NSA and the UK's NCSC recommend post-quantum cryptography as the main defense and say not to rely on QKD alone [1][4].

## Sources

1. NSA, "Quantum Key Distribution (QKD) and Quantum Cryptography (QC)." https://www.nsa.gov/Cybersecurity/Quantum-Key-Distribution-QKD-and-Quantum-Cryptography-QC/
2. Evans et al., "Trusted node QKD at an electrical utility," IEEE Access 9, 105220 (2021). https://arxiv.org/abs/2103.09877
3. Briegel, Dür, Cirac, and Zoller, "Quantum repeaters," Phys. Rev. Lett. 81, 5932 (1998). https://arxiv.org/abs/quant-ph/9803056
4. UK NCSC, "Quantum security technologies." https://www.ncsc.gov.uk/paper/quantum-security-technologies
5. NIST FIPS 203 and 204 (2024). https://csrc.nist.gov/projects/post-quantum-cryptography
6. Bennett et al., "Teleporting an unknown quantum state via dual classical and Einstein-Podolsky-Rosen channels," Phys. Rev. Lett. 70, 1895 (1993).