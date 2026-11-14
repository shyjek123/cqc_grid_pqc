# Step 1 Write-up

This run used Qiskit Aer and qBraid. It is a circuit experiment, not a fiber QKD link. Counts below are this experiment’s results.

## What the runs showed

With no eavesdropper, 200 qubits gave a sifted key of 93 bits, the two keys matched, and the quantum bit error rate (QBER) was 0%. With Eve measuring every qubit in a random basis and resending, QBER was 21.5%. A second full-interception run was 24.7%. A teammate’s run of the same attack was 33.3%.

An intercept-resend attack is expected to leave about 25% errors in the sifted key: Eve guesses the basis wrong half the time, and Bob is then wrong half of those times [1].

A partial-interception sweep, in 10% steps, generally rose with the fraction Eve touched. It was 8.2% at 40% interception and 12.1% at 50%. The 90% point (29.9%) came out higher than the 100% point (24.5%). A teammate’s 40% test was 16.1% and their 50% test was 8.6%, each from 200 qubits. Small samples move around.

## The 11% line

For the usual one-way proof, BB84 can still distill a key when the bit and phase error rates are under 11% [2]. That is a security bound, not a field alarm setting. Under the 25% model, 11% QBER corresponds to Eve touching about 11/25 = 44% of the qubits. This sample first crossed 11% between 40% and 50% interception. A smaller sample can cross early or late. Below 11% does not mean Eve was absent [2].

## Hardware

| Environment | QBER | Shots |
|---|---|---|
| Qiskit Aer, IonQ cloud simulator, qBraid QIR | 0% | — |
| Quantinuum H2 emulator | 0.25% | 200 |
| IonQ Forte-1 (`aws:ionq:qpu:forte-1`) | 0.17% | 100 |
| Rigetti Cepheus-1-108Q (teammate) | 2.9% | 200 |

Job IDs: IonQ `aws:ionq:qpu:forte-1-0b8e-qjob-6af871b2c8f5265fb3f1b2c6`; Quantinuum `quantinuum:quantinuum:sim:h2-emulator-0b8e-qjob-6af7cef9f15852ed27b722aa`; Rigetti `aws:rigetti:qpu:cepheus-1-108q-57e1-qjob-6af7cf8ff15852ed27b722ca`.

Ideal simulators were at 0%. The two QPUs were not. These are processor errors, not fiber errors, and the runs differ in device and shots, so they do not rank the two technologies.

## A real utility fiber

On an electric-utility fiber, one polarization BB84 link measured 3.9% ± 1.3% QBER. Wind on aerial fiber made the polarization tracker lose lock and the error rate jump [3]. A different system on that network marked a key “compromised” when its own internal QBER passed 13% [3]. That 13% is that box’s label, not the measured 3.9%, and not the 11% proof bound.

Our 0.17% and 2.9% QPU figures are not comparable to that 3.9% fiber figure.

## What this does not provide

BB84 does not authenticate the sender. Without an authenticated classical channel, someone in the middle can run a separate link with each side. Authentication needs a pre-shared key or a quantum-safe signature [4][5].

QKD makes key material. It does not by itself encrypt traffic or sign messages. NSA does not recommend QKD for National Security Systems unless its stated limits are overcome, including the lack of source authentication, the need for special fiber, trusted relays, and the gap between the physics proof and the built hardware [4]. NCSC does not endorse QKD for UK government or military use and says critical networks should not rely on QKD alone. Its primary mitigation is quantum-safe cryptography [5].

Attacks on real receivers, including bright-light blinding and time-shift, have broken commercial systems without breaking the BB84 proof [6][7]. This notebook also does not do error correction or privacy amplification.

## Sources

1. Gisin, Ribordy, Tittel, and Zbinden, “Quantum cryptography,” Rev. Mod. Phys. 74, 145 (2002). https://arxiv.org/abs/quant-ph/0101098. Intercept-resend gives a 25% error rate.
2. Shor and Preskill, “Simple proof of security of the BB84 quantum key distribution protocol,” Phys. Rev. Lett. 85, 441 (2000). https://arxiv.org/abs/quant-ph/0003004. One-way post-processing works below an 11% error rate.
3. Evans et al., “Trusted node QKD at an electrical utility,” IEEE Access 9, 105220 (2021). https://arxiv.org/abs/2103.09877. Link A–B: 3.9% ± 1.3% QBER. QKD1 labels a key compromised above an internal 13% QBER.
4. NSA, “Quantum key distribution (QKD) and quantum cryptography (QC).” https://www.nsa.gov/Cybersecurity/Quantum-Key-Distribution-QKD-and-Quantum-Cryptography-QC/
5. UK NCSC, “Quantum security technologies.” https://www.ncsc.gov.uk/paper/quantum-security-technologies
6. Lydersen et al., “Hacking commercial quantum cryptography systems by tailored bright illumination,” Nature Photonics 4, 686 (2010). https://doi.org/10.1038/nphoton.2010.214
7. Zhao, Fung, Qi, Chen, and Lo, “Quantum hacking: experimental demonstration of time-shift attack against practical quantum-key-distribution systems,” Phys. Rev. A 78, 042333 (2008). https://doi.org/10.1103/PhysRevA.78.042333
