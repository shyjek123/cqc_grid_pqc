# BB84 Quantum Key Distribution Experiment

## 1. Introduction

This experiment investigates how BB84 quantum key distribution (QKD) can establish a shared secret key and detect eavesdropping. I implemented BB84 using Qiskit Aer and compared the results with quantum simulators, emulators, and real quantum hardware through qBraid.

The main objectives were to measure the quantum bit error rate (QBER) with and without interception, examine how partial interception affects detection, and compare noise across different hardware systems.

The results are intended to support our team's Q-Day Readiness Planner for a city power utility.

## 2. Shared Key Generation

The first experiment tests whether Alice and Bob can establish matching keys without an eavesdropper. Alice randomly selects a bit and a basis, while Bob independently selects a measurement basis.

After transmission, Alice and Bob retain only the bits where their bases match. These bits form their sifted keys.

### Results

- Qubits transmitted: 200
- Sifted key length: 93 bits
- QBER without Eve: 0.00%
- Alice and Bob's keys match: True

The results show that Alice and Bob successfully generated matching sifted keys without errors in the ideal simulation.

## 3. Eavesdropping Detection

The second experiment introduces Eve, who intercepts each qubit, measures it using a random basis, and sends a replacement qubit to Bob.

When Eve uses the wrong basis, she can change the quantum state and introduce errors.

### Results

- QBER without Eve: 0.00%
- QBER with Eve: 21.51%
- Theoretical QBER with full interception: 25%

The measured QBER increased from 0.00% to 21.51%, close to the theoretical 25%.

Our team independently ran the same attack and measured 33.3% QBER. A second full-interception experiment produced 24.7%. The differences are caused by random sampling and the relatively small number of sifted bits.

These results demonstrate that BB84 can detect potential interception through changes in QBER. However, a high error rate does not necessarily confirm eavesdropping because noise and hardware errors can produce similar effects.

## 4. Partial Interception Experiment

I tested Eve intercepting between 0% and 100% of the transmitted qubits in increments of 10%. This experiment used a classical Monte Carlo simulation of the ideal BB84 measurement probabilities.

### Experimental Results

| Eve Interception | Measured QBER |
|---|---|
| 0% | 0.00% |
| 10% | 1.82% |
| 20% | 2.82% |
| 30% | 6.12% |
| 40% | 8.24% |
| 50% | 12.12% |
| 60% | 13.88% |
| 70% | 14.59% |
| 80% | 18.89% |
| 90% | 29.92% |
| 100% | 24.48% |

The measured QBER generally increased as Eve intercepted more qubits. At 40% interception, QBER was 8.24%, below the example 11% threshold. At 50% interception, QBER increased to 12.12%, exceeding the threshold.

The results also showed variation from random sampling. For example, the 90% interception test produced a higher QBER than the 100% test.

Our teammate's experiment showed similar uncertainty. Their 40% interception test produced 16.1% QBER, while their 50% test produced 8.6%. Each test used 200 transmitted qubits and retained roughly half after sifting.

These results show that smaller samples can produce inconsistent QBER estimates, making partial interception harder to distinguish from normal noise.

### Figure 1. BB84 Partial Interception

![Figure 1. BB84 partial-interception results](bb84_partial_interception_results.png)

Figure 1 compares the measured QBER, theoretical QBER, and example 11% abort threshold. The 0.17% IonQ QPU baseline is included as a separate hardware measurement.

## 5. Hardware Testing and Comparison

The next experiment compared BB84 on local simulators, emulators, and real quantum computers.

My hardware test used IonQ Forte-1 through AWS on qBraid. The circuit contained 16 qubits and ran for 100 shots.

Our teammate conducted an additional hardware experiment using the Rigetti Cepheus-1-108Q superconducting quantum computer with 200 shots.

### Experimental Results

| Testing Environment | Type | QBER |
|---|---|---|
| Qiskit Aer | Local simulator | 0.00% |
| IonQ cloud simulator | Cloud simulator | 0.00% |
| qBraid QIR | Cloud simulator | 0.00% |
| Quantinuum H2 | Hardware emulator | 0.25% |
| IonQ Forte-1 | Real QPU | 0.17% |
| Rigetti Cepheus-1-108Q | Real QPU | 2.90% |

The ideal simulators produced no errors. The Quantinuum H2 emulator produced a small error rate, while the real quantum computers produced different levels of noise.

IonQ Forte-1 measured 0.17% QBER, compared with 2.9% on Rigetti Cepheus-1-108Q.

The processors use different technologies. IonQ uses trapped-ion qubits, while Rigetti uses superconducting qubits.

In our teammate's Rigetti experiment, transmitted 1s produced more errors than transmitted 0s. One possible explanation is relaxation of the excited qubit state before measurement, which can cause a 1 to be measured as a 0.

The different QBER measurements demonstrate that hardware noise depends on the equipment and implementation. However, the tests used different processors and execution conditions, so they do not establish that one technology is generally more accurate than the other.

These experiments measured errors in quantum computing circuits, not in actual fiber-optic QKD links.

### Figure 2. Hardware and Simulator Comparison

![Figure 2. BB84 hardware comparison](bb84_hardware_comparison.png)

Figure 2 compares simulator, emulator, and QPU error rates from our team's experiments.

### Hardware Job Information

**IonQ Forte-1 — My experiment**

- Device: `aws:ionq:qpu:forte-1`
- Shots: 100
- QBER: 0.17%
- Status: COMPLETED
- Job ID: `aws:ionq:qpu:forte-1-0b8e-qjob-6af871b2c8f5265fb3f1b2c6`

**Quantinuum H2 — My experiment**

- Shots: 200
- QBER: 0.25%
- Job ID: `quantinuum:quantinuum:sim:h2-emulator-0b8e-qjob-6af7cef9f15852ed27b722aa`

**Rigetti Cepheus-1-108Q — Teammate's experiment**

- Shots: 200
- QBER: 2.90%
- Job ID: `aws:rigetti:qpu:cepheus-1-108q-57e1-qjob-6af7cf8ff15852ed27b722ca`

## 6. Error Threshold Analysis

The experiment uses an example 11% QBER threshold to examine when a key should be rejected.

Under the ideal intercept-resend model, expected QBER is approximately 25% multiplied by the intercepted fraction.

The theoretical interception percentage corresponding to an 11% QBER is:

0.11 / 0.25 = 0.44, or 44%

My measured results first exceeded the threshold between 40% and 50% interception.

However, this does not mean interception below 44% will always remain undetected. Detection depends on the number of sampled bits, normal noise, and the statistical security analysis.

Our teammate's experiment further demonstrated this uncertainty when the 40% interception test exceeded the threshold but the 50% test did not.

For an actual utility, the normal QBER should be measured on the communication link before establishing an operating threshold. A sufficient sample size is necessary to avoid false alarms and missed attacks.

The approximately 11% BB84 security limit is not a universal alarm setting. Even below this limit, usable secret-key generation depends on the error-correction and privacy-amplification procedures and the system's security assumptions.

## 7. Security Advantages and Limitations

BB84 uses quantum mechanics to detect potential eavesdropping. Measuring a qubit using the wrong basis can disturb its state, while the no-cloning theorem prevents an attacker from perfectly copying an unknown quantum state.

Unlike traditional public-key key exchange, BB84 can provide evidence of interference through changes in the error rate.

However, BB84 still requires an authenticated classical communication channel. Without authentication, an attacker could impersonate Alice or Bob and establish separate keys with each participant.

Authentication could use a pre-shared secret or an appropriate post-quantum signature system, such as ML-DSA.

Real QKD systems also have hardware vulnerabilities. Detector-blinding and time-shift attacks demonstrate that attackers may exploit equipment behavior rather than directly breaking the underlying quantum protocol.

The NSA does not recommend QKD for protecting National Security Systems under current implementation limitations. The UK NCSC also cautions against relying solely on QKD for critical infrastructure and recommends quantum-safe cryptography as the primary mitigation.

Additional limitations of our experiment include the small sample sizes, simplified attack model, and lack of an actual fiber-optic QKD connection. The notebook also does not implement a complete authenticated key-generation system with error correction and privacy amplification.

## 8. Application to Power Utility Networks

The results can be applied to the evaluation of secure communications between power utility control centers and substations.

A field study by Evans et al. demonstrated QKD using three systems connected through a real electrical utility fiber network. One BB84 link measured approximately 3.9% QBER, with variation caused partly by environmental conditions affecting the fiber. Another system in the demonstration classified keys as compromised when its internal QBER exceeded 13%.

This study shows that real utility communication links introduce noise that must be considered when evaluating possible interception.

Our experiments produced 0.17% QBER on IonQ Forte-1 and 2.9% on Rigetti Cepheus-1-108Q. These values are not directly comparable with the field study because they were measured on quantum processors rather than optical fiber links.

For our Q-Day Readiness Planner, the findings support evaluating QKD for selected high-priority communication links while using post-quantum cryptography for the broader utility network.

QKD would require specialized equipment, authenticated communication, and potentially trusted relay nodes. The utility would need to compare those costs with software-based post-quantum cryptography before selecting a deployment strategy.

## 9. Conclusion

The BB84 experiment demonstrated matching sifted keys and a measurable increase in QBER when an eavesdropper intercepted the transmission.

The initial simulation produced 0.00% QBER without Eve and 21.51% with Eve. The partial-interception experiment showed that smaller attacks could produce error rates below the example 11% threshold.

Real hardware experiments measured 0.17% QBER on IonQ Forte-1 and 2.9% on Rigetti Cepheus-1-108Q. These results demonstrate that quantum hardware can introduce errors without an eavesdropper and that noise varies between systems.

The experiments support the potential use of BB84 for detecting interference during key distribution. However, implementing QKD for a power utility would require testing on actual fiber links, establishing reliable error thresholds, and addressing authentication, equipment vulnerabilities, and deployment costs.

## 10. References

1. qBraid. *Tennessee Quantum Hackathon — Secure the Grid*. https://github.com/qBraid/tn-quantum-hackathon/tree/main/1-utc-secure-the-grid

2. Evans, P. G., et al. (2021). *Trusted Node QKD at an Electrical Utility*. IEEE Access, 9, 105220–105229. https://arxiv.org/abs/2103.09877

3. National Security Agency. *Quantum Key Distribution (QKD) and Quantum Cryptography (QC)*. https://www.nsa.gov/Cybersecurity/Quantum-Key-Distribution-QKD-and-Quantum-Cryptography-QC/

4. National Security Agency. (2026). *Quantum Cryptographic Solutions Are Limited Compared to Post-Quantum Algorithms*. https://www.nsa.gov/Cybersecurity/Post-Quantum-Cryptography-Resource-Hub/Article-Display/Article/4616320/quantum-cryptographic-solutions-are-limited-compared-to-post-quantum-algorithms/

5. UK National Cyber Security Centre. (2026). *Quantum Security Technologies*. https://www.ncsc.gov.uk/paper/quantum-security-technologies

6. Lydersen, L., et al. (2010). *Hacking Commercial Quantum Cryptography Systems by Tailored Bright Illumination*. Nature Photonics. https://doi.org/10.1038/nphoton.2010.214

7. Zhao, Y., et al. (2008). *Experimental Quantum Key Distribution with a Simulated Time-Shift Attack*. Physical Review A, 78. https://doi.org/10.1103/PhysRevA.78.042333