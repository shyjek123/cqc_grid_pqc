# Step 3 Write-up

## The link

Two sites, a control center and a substation. The quantum channel carries one half of an entangled pair. The classical channel carries two correction bits and has to be authenticated.

Teleportation sends an unknown qubit using one shared entangled pair and two classical bits [1]. The notebook’s circuit, all on one chip:

1. `ry(1.0)` then `rz(0.7)` on qubit 0, a state that is not 0 or 1.
2. `h(1)`, `cx(1, 2)` to entangle qubits 1 and 2.
3. `cx(0, 1)`, `h(0)` for the sender’s Bell measurement.
4. `cx(1, 2)`, `cz(0, 2)` as the receiver’s corrections, applied as gates rather than `if_test`.
5. `rz(-0.7)` then `ry(-1.0)` on qubit 2, undoing the state that was sent.
6. Measure all three qubits last.

On a real link the sender measures first and sends the two bits. Applying the corrections before measuring is the same circuit under the deferred-measurement principle. The check is that qubit 2, the high bit in Qiskit’s print order, is 0. The notebook asks for 1024 shots on the noise-free simulator and 200 shots on IonQ’s simulator with noise model `forte-1`. Those runs are not in the file.

This shows the logic. It does not show a length of fiber.

## Trusted nodes

Fiber loss is why long QKD uses relays. A trusted relay ends one key and starts the next, so it sees the key. A utility deployment has already been run that way: three QKD systems on a real electric-utility fiber, with trusted nodes passing keys [2].

A quantum repeater is a different job. An intermediate node swaps entanglement by a Bell measurement and forwards the two classical outcomes [3]. Those outcomes do not reveal the teleported qubit. The node is not holding the key the way a trusted QKD relay does. Repeaters of that kind are a proposed architecture [3], not equipment this design assumes is already in the field. The notebook’s three qubits are on one chip, so it does not demonstrate a repeater.

Teleportation still does not authenticate the far end. QKD protocols do not provide authentication, so the classical channel still needs a pre-shared key or a post-quantum signature [4][5].

## What to deploy

NSA does not recommend QKD for National Security Systems unless its limits are overcome, and it points out that trusted relays add cost and insider risk [4]. NCSC does not endorse QKD for UK government or military use, and says not to rely on it alone for critical networks. Quantum-safe cryptography is the primary mitigation [5].

So the default is software: ML-KEM (FIPS 203) for key establishment and ML-DSA (FIPS 204) for signatures [6]. NIST deprecates quantum-vulnerable public-key algorithms after 2030 and disallows them under NIST standards after 2035 [7]. The quantum link, if built, is one metro fiber pair where the hardware cost is accepted. If it aborts, traffic uses the ML-KEM path. The two secrets can be mixed with HKDF [8]; that is a design choice, not a claim that either secret alone has been proved sufficient.

Rollout: inventory the fiber; put hybrid ML-KEM on remote access and wide-area links first, so an abort already has a path; pilot one control-center-to-substation pair; authenticate the classical channel; feed the result into the existing cipher. Do not start with radio. In-substation GOOSE is a different protocol from the wide-area links.

## Sources

1. Bennett, Brassard, Crépeau, Jozsa, Peres, and Wootters, “Teleporting an unknown quantum state via dual classical and Einstein-Podolsky-Rosen channels,” Phys. Rev. Lett. 70, 1895 (1993).
2. Evans et al., “Trusted node QKD at an electrical utility,” IEEE Access 9, 105220 (2021). https://arxiv.org/abs/2103.09877
3. Briegel, Dür, Cirac, and Zoller, “Quantum repeaters: the role of imperfect local operations in quantum communication,” Phys. Rev. Lett. 81, 5932 (1998). Entanglement swapping at the intermediate node.
4. NSA, “Quantum key distribution (QKD) and quantum cryptography (QC).” https://www.nsa.gov/Cybersecurity/Quantum-Key-Distribution-QKD-and-Quantum-Cryptography-QC/
5. UK NCSC, “Quantum security technologies.” https://www.ncsc.gov.uk/paper/quantum-security-technologies
6. NIST FIPS 203 (ML-KEM) and FIPS 204 (ML-DSA), 13 August 2024. https://csrc.nist.gov/projects/post-quantum-cryptography
7. NIST IR 8547 (2026). https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8547.pdf
8. Krawczyk and Eronen, “HMAC-based Extract-and-Expand Key Derivation Function (HKDF),” RFC 5869 (2010). https://www.rfc-editor.org/rfc/rfc5869
