# Step 1: Catch the Eavesdropper

## Results

| Run | QBER |
|---|---|
| No eavesdropper | 0% (sifted keys match) |
| Eavesdropper intercepts every qubit | 26.9% |

The expected rate with an eavesdropper is 25% [1]. The lab gives 18% to 33% as normal for 200 rounds. Note: the notebook checks every sifted bit; real BB84 checks only a random sample.

## Hardware

| Device | QBER | Shots | Job ID |
|---|---|---|---|
| Qiskit Aer (local simulator) | 0% | 200 | — |
| IonQ simulator, `aria-1` noise | 0% | 200 | `ionq:ionq:sim:simulator-d6f1-qjob-6af8ecc8c8f5265fb3f214b4` |
| Quantinuum H2 emulator | 0.25% | 200 | `quantinuum:quantinuum:sim:h2-emulator-0b8e-qjob-6af7cef9f15852ed27b722aa` |
| IonQ Forte-1 (real QPU) | 0.17% | 100 | `aws:ionq:qpu:forte-1-0b8e-qjob-6af871b2c8f5265fb3f1b2c6` |

**Threshold:** BB84 can still produce a secure key below about 11% QBER [2]. Normal noise here was under 1%, and an eavesdropper causes about 25%, so an 11% cutoff separates the two. On a real utility fiber, normal noise was 3.9% [3], so the cutoff should be set above the link's measured baseline and below 11%.

## Why it works

Alice sends each bit in one of two bases. Measuring in the wrong basis gives a random result and changes the qubit. Eve can't copy a qubit to check it first (no-cloning theorem) [4]. She guesses the wrong basis half the time, and then Bob reads the wrong bit half of those times: ½ × ½ = 25% errors [1]. Those errors are how Eve gets caught.

## For the utility

The error rate works as a tap alarm on a fiber link. It only works if the two sides can confirm who they're talking to, which BB84 doesn't do on its own [5].

## Sources

1. Gisin et al., "Quantum cryptography," Rev. Mod. Phys. 74, 145 (2002). https://arxiv.org/abs/quant-ph/0101098
2. Shor and Preskill, "Simple proof of security of the BB84 quantum key distribution protocol," Phys. Rev. Lett. 85, 441 (2000). https://arxiv.org/abs/quant-ph/0003004
3. Evans et al., "Trusted node QKD at an electrical utility," IEEE Access 9, 105220 (2021). https://arxiv.org/abs/2103.09877
4. Wootters and Zurek, "A single quantum cannot be cloned," Nature 299, 802 (1982). https://doi.org/10.1038/299802a0
5. UK NCSC, "Quantum security technologies." https://www.ncsc.gov.uk/paper/quantum-security-technologies
