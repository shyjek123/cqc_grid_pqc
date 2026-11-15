# Step 2b: Search for the Key

## Results

Secret key: 2 (binary `10`). For N = 4 keys: 2 qubits, 1 Grover iteration.

| Run | Shots on key 2 |
|---|---|
| Qiskit Aer simulator | 1024 / 1024 |
| IonQ simulator, `forte-1` noise model | 200 / 200 |

IonQ job ID: `ionq:ionq:sim:simulator-d6f1-qjob-6af8fa66c8f5265fb3f219f9`

For N = 4, one iteration lands on the key every time. Noise had no visible effect, because this circuit has only 2 two-qubit gates. The lab notes that N = 8 needs about 24 and N = 16 about 84, so noise will matter more as N grows.

## What it means for AES

Grover's search finds a key among N in about √N steps instead of N [1]. On paper, that halves key strength: AES-128 drops to about 64 bits, and AES-256 to about 128.

NIST says AES-128 is still fine: "AES 128 will remain secure for decades to come." Grover's steps must run one after another, so they can't be split across many machines, and quantum hardware costs more per step [2]. Current applications can keep using AES-128, AES-192, or AES-256 [2].

## Compared with RSA

Shor's algorithm completely breaks RSA, so RSA must be replaced with new algorithms like ML-KEM and ML-DSA [3]. Grover only weakens AES, and at most the fix is a longer key.

**Deck line:** Symmetric keys come last in the migration plan. Replace RSA first.

## Sources

1. Grover, "A fast quantum mechanical algorithm for database search," Proceedings of STOC 1996, 212–219. https://arxiv.org/abs/quant-ph/9605043
2. NIST, Post-Quantum Cryptography FAQs, "Should we double the key length for AES now?" https://csrc.nist.gov/projects/post-quantum-cryptography/faqs
3. NIST FIPS 203 (ML-KEM) and FIPS 204 (ML-DSA), 2024. https://csrc.nist.gov/projects/post-quantum-cryptography