# Step 2b Write-up

## The search

Grover’s algorithm finds one marked item among \(N\) in about \((\pi/4)\sqrt{N}\) steps [1]. Each step marks the right item and then amplifies it. Getting the full square-root speedup requires those steps in series; Zalka showed they cannot all be farmed out in parallel [2].

The notebook uses the marked item as a stand-in for a key. Its settings:

| \(N\) | Qubits | Iterations |
|---|---|---|
| 4 | 2 | 1 |
| 8 | 3 | 2 |
| 16 (optional) | 4 | 3 |

The secret key in the notebook is 2. The notebook’s own note on size: about 2 two-qubit gates at \(N = 4\), about 24 at \(N = 8\), and about 84 at \(N = 16\). The oracle is built from the known answer. A real key search would run AES itself as the oracle, once per step, in series. This notebook does not do that.

## AES key length

Counting only the steps, a \(k\)-bit key falls to about \(k/2\) bits: AES-128 to 64, AES-192 to 96, AES-256 to 128.

NIST’s post-quantum FAQ says not to stop at that count. Quantum hardware is expected to cost more per operation than classical hardware, and the full speedup is serial, so a real parallel attack gains less than \(\sqrt{N}\) [2]. NIST’s words: “it is quite likely that Grover’s algorithm will provide little or no advantage in attacking AES, and AES 128 will remain secure for decades to come.” AES-192 and AES-256 “will still be safe for a very long time,” if no new weakness is found in AES. Current applications can keep AES-128, AES-192, or AES-256. Anything with less than 112 bits of classical security should not be used [2].

So Grover is a reason to drop keys under that 112-bit classical floor. It is not, on NIST’s stated view, a reason to treat AES-128 as broken.

## Compared with RSA

Shor’s algorithm breaks RSA and elliptic-curve cryptography. Those have to be replaced: ML-KEM (FIPS 203) for key establishment and ML-DSA (FIPS 204) for signatures [3][4]. There is no longer RSA key that survives Shor.

Grover does not break AES. NIST says keep the AES sizes above, and it will say later if a symmetric-key change is actually required [2]. Retire RSA and elliptic-curve uses first.

## Sources

1. Grover, “A fast quantum mechanical algorithm for database search,” Proceedings of STOC 1996, 212–219. The iteration count \((\pi/4)\sqrt{N}\) is the standard optimum; see Boyer, Brassard, Høyer, and Tapp, Fortschr. Phys. 46, 493 (1998).
2. NIST, Post-quantum cryptography FAQs, “Should we double the key length for AES now?” (added 18 November 2018). https://csrc.nist.gov/projects/post-quantum-cryptography/faqs. The FAQ is the source for the AES-128 conclusion, the 112-bit classical floor, and the attribution to Zalka (1997) that the full speedup is serial.
3. Shor, “Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer,” SIAM J. Comput. 26, 1484 (1997).
4. NIST FIPS 203 (ML-KEM) and FIPS 204 (ML-DSA), 13 August 2024. https://csrc.nist.gov/projects/post-quantum-cryptography
