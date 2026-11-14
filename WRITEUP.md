# Step 1: Catch the Eavesdropper — BB84

## Part 1: Shared Key Without an Eavesdropper

The BB84 simulation tests whether Alice and Bob can establish a matching secret key using quantum bits. Alice randomly chooses a bit and a measurement basis, while Bob independently chooses a basis for measuring each received qubit.

After transmission, Alice and Bob compare their basis choices and keep only the measurements where their bases match. These retained bits form their sifted keys.

**Simulation results:**
- Number of qubits transmitted: 200
- QBER without Eve: **[INSERT ACTUAL RESULT]**
- Matching sifted key bits: **[INSERT NUMBER]**

In an ideal, noise-free simulation without an eavesdropper, the expected QBER is 0%, meaning Alice and Bob's sifted keys match.

## Part 2: Detecting an Eavesdropper

The simulation introduces Eve, who intercepts Alice's qubits, measures them using randomly selected bases, and then sends replacement qubits to Bob.

When Eve measures using the wrong basis, she may change the quantum state. This introduces errors that Alice and Bob can detect when they compare a sample of their sifted key bits.

**Simulation results:**
- QBER without Eve: **[INSERT ACTUAL RESULT]**
- QBER with Eve intercepting every qubit: **[INSERT ACTUAL RESULT]**
- Increase in QBER: **[INSERT DIFFERENCE]**

The expected QBER for an ideal intercept-resend attack is approximately 25%. A substantial increase in QBER provides evidence of interference or noise on the communication channel, though it does not by itself prove that an eavesdropper is present.

## Part 3: Hardware Noise and Abort Threshold

The notebook groups 16 BB84 rounds into one quantum circuit and runs it with 200 shots. This allows the simulation or hardware to measure the error rate without submitting hundreds of separate jobs.

| Experiment | QBER | Job ID |
|---|---|---|
| Local Qiskit Aer simulator | [RESULT] | Local; no cloud job |
| IonQ simulator (if run) | [RESULT] | [JOB ID] |
| Quantinuum H2 emulator (if run) | [RESULT] | [JOB ID] |
| Real quantum hardware | [RESULT] | [JOB ID] |

Real quantum hardware can introduce measurement errors and other imperfections even when no eavesdropper is present.

**Threshold decision:**

The utility should estimate the normal error rate of its communication equipment and compare it with the observed QBER. An unexpectedly high error rate should cause the key to be discarded rather than used.

For the simulated intercept-resend example, an 11% threshold is a useful educational reference, but it is not a universal deployment setting. Real systems must account for sample size, equipment noise, statistical uncertainty, error correction, and the security of privacy amplification.

**Our chosen threshold:** [INSERT THRESHOLD AND JUSTIFICATION]

**Hardware findings:** [COMPARE THE MEASURED ERROR RATES AND EXPLAIN WHETHER THE THRESHOLD IS APPROPRIATE]

## Part 4: What Quantum Physics Provides

BB84 uses quantum properties to detect possible interception during key distribution. Because measuring a quantum state using an incompatible basis can disturb it, an attacker cannot freely copy and measure unknown quantum states without risking detectable errors.

Traditional public-key key exchange relies on mathematical security assumptions rather than this particular physical disturbance mechanism.

However, BB84 does not automatically authenticate the participants. Alice and Bob still need an authenticated classical communication channel so an attacker cannot impersonate one of them. Quantum-safe authentication is especially important for long-term infrastructure security.

Real quantum key distribution equipment can also be vulnerable to implementation attacks, including detector manipulation and side-channel attacks. QKD requires specialized hardware, and its practical security depends on the equipment and network design.

The NSA does not recommend QKD for protecting U.S. National Security Systems unless major limitations are overcome. The UK's NCSC also cautions against relying on QKD alone for critical infrastructure and recommends quantum-safe cryptography as the preferred general mitigation.

## Presentation: What the Error-Rate Increase Means for a Utility

**Demonstration:** Compare the measured QBER with Eve disabled and enabled.

**Main finding:** Intercepting quantum key transmissions introduces detectable errors in an ideal BB84 implementation.

**Utility relevance:** A power utility could investigate QKD for selected high-value fiber links between control centers and substations, where monitoring potential interception may provide additional security benefits.

**Limitations:** The simulation does not demonstrate a production-ready QKD link. Practical deployment requires authentication, specialized equipment, error correction, privacy amplification, and validation against real hardware vulnerabilities.

**Recommended next step:** Compare a limited QKD pilot with a software-based post-quantum cryptography upgrade before selecting a deployment strategy.

## References

- qBraid, *Tennessee Quantum Hackathon — Secure the Grid*, `1_bb84_eavesdropper.ipynb`.
- National Security Agency, *Quantum Key Distribution (QKD) and Quantum Cryptography (QC)*.
- UK National Cyber Security Centre, *Quantum Security Technologies*, 2026.
- NIST, *What Is Quantum Cryptography?*
