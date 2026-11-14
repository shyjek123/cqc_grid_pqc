# Step 2a Write-up

## Factoring 15

The period-finding run returned phases 0, 1/4, 1/2, and 3/4.

The multiply-by-7-mod-15 step is hand-built for 15. It does not factor 21, and it is not the circuit for RSA-2048. Shor’s algorithm is what makes factoring and discrete logarithms efficient on a large enough quantum computer, which is why RSA and elliptic-curve cryptography fall [1].

## How far the hardware is

On 13 November 2026 the author listed gate-model QPUs on qBraid once each and left out analog machines (QuEra Aquila, Pasqal Fresnel), which cannot run this circuit. That list is an observation, not a published catalog. The largest entry was 156 qubits (IBM Marrakesh, Pittsburgh, Kingston, Fez, and Boston). Also listed: IBM Miami 120; Rigetti Cepheus-1-108Q 107; IQM Emerald 54; IonQ Forte 1, IonQ Forte Enterprise 1, and Rigetti Cepheus-1-36Q 36; IQM Garnet 20; AQT IBEX Q1 12.

Published estimates for factoring RSA-2048, all at a \(10^{-3}\) physical error rate, a 1 µs cycle, and a 10 µs reaction time:

| Estimate | Physical qubits | Time | Wiring assumed |
|---|---|---|---|
| Gidney and Ekerå, 2019 / Quantum 2021 [2] | 20 million | 8 hours | nearest-neighbor grid |
| Gidney, 2025 [3] | 897,864 (1,409 logical active; 1,537 including idle workspace) | under a week (about 5 days before rounding) | same nearest-neighbor grid |
| Webster et al., 2026 [4] | fewer than 100,000 | one month | quantum LDPC; not a nearest-neighbor grid |

Using the author’s 156-qubit maximum, 897,864 / 156 is about 5,800. That ratio is only a qubit count. It leaves out error correction, the assumed error rate, and hours-to-a-month of fault-tolerant runtime [2][3].

## What a utility should move first

Shor breaks RSA and elliptic-curve key establishment and signatures [1]. Three uses follow.

Recorded VPN handshakes (IPsec or TLS) can be decrypted later. Those VPNs are how remote access crosses the electronic security perimeter in NERC CIP-005 [5].

The same key establishment sits under wide-area SCADA (DNP3, ICCP/TASE.2, IEC 61850 MMS over TLS or IPsec). Later decryption exposes operating data. A later forged signature can pass as a command. In-substation GOOSE is a different protocol from those wide-area links.

Firmware signatures on relays, RTUs, and gateways can be forged later, and the bad image stays for the life of the device. Mosca’s test is whether the years the data must stay secret, plus the years to migrate, already exceed the years until the cryptosystem can be broken [6].

NIST will deprecate quantum-vulnerable public-key algorithms after 2030 and disallow them under NIST standards after 2035 [7]. Replacements: ML-KEM (FIPS 203) for key establishment, ML-DSA (FIPS 204) for general signatures, SLH-DSA (FIPS 205) where a stateless hash-based signature is wanted, and LMS or XMSS (SP 800-208) only where the private-key state can be kept from reuse [8][9].

Order: inventory every RSA and elliptic-curve use; remote-access VPNs first, because traffic can be recorded now and a concentrator is a software change; firmware-signing roots next; wide-area SCADA and ICCP with those certificates; symmetric keys after that. Grover’s algorithm is a square-root search speedup, not a break of AES [10].

## Sources

1. Shor, “Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer,” SIAM J. Comput. 26, 1484 (1997).
2. Gidney and Ekerå, “How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits,” Quantum 5, 433 (2021). https://arxiv.org/abs/1905.09749
3. Gidney, “How to factor 2048 bit RSA integers with less than a million noisy qubits” (2025). https://arxiv.org/abs/2505.15917. 1,409 active logical qubits, 1,537 including idle workspace, 897,864 physical qubits, about 4.96 days, reported as under a week.
4. Webster et al., “The Pinnacle architecture: reducing the cost of breaking RSA-2048 to 100 000 physical qubits using quantum LDPC codes” (2026). https://arxiv.org/abs/2602.11457. Fewer than 100,000 physical qubits in an expected one month, at \(p = 10^{-3}\), 1 µs cycle, 10 µs reaction time. This needs connectivity beyond a nearest-neighbor grid.
5. NERC Reliability Standard CIP-005, Cyber Security — Electronic Security Perimeter. https://www.nerc.com/standards
6. Mosca, “Cybersecurity in an era with quantum computers: will we be ready?,” IEEE Security & Privacy 16, no. 5 (2018).
7. NIST IR 8547, “Transition to Post-Quantum Cryptography Standards” (2026). https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8547.pdf. Deprecate quantum-vulnerable public-key cryptography after 2030; disallow it under NIST standards after 2035.
8. NIST FIPS 203, 204, and 205 (13 August 2024). https://csrc.nist.gov/projects/post-quantum-cryptography. ML-KEM, ML-DSA, SLH-DSA.
9. NIST SP 800-208, “Recommendation for Stateful Hash-Based Signature Schemes” (2020). LMS and XMSS. https://csrc.nist.gov/projects/stateful-hash-based-signatures
10. NIST, Post-quantum cryptography FAQs, “Should we double the key length for AES now?” (added 18 November 2018). https://csrc.nist.gov/projects/post-quantum-cryptography/faqs
