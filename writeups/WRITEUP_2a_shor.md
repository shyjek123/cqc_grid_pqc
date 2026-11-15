# Step 2: Harvest Now, Decrypt Later

## Factoring 15

The most common measurement was `11000000`, a phase of 0.75 = 3/4, so the period is r = 4. Check: 7⁴ mod 15 = 1. Then gcd(7² − 1, 15) = **3** and gcd(7² + 1, 15) = **5**, and 3 × 5 = 15.

**What this proves:** `c_amod15_a7` is hand-built for N = 15 and a = 7. It doesn't work for N = 21 or a 2048-bit number. The demo shows that a measured period gives the factors. It doesn't show that today's hardware can run the much larger circuit needed for RSA-2048.

## The hardware gap

Real gate-based devices on qBraid, each counted once:

| Device | Qubits |
|---|---|
| Rigetti Cepheus-1-108Q | 107 |
| IQM Emerald | 54 |
| IonQ Forte-1, IonQ Forte Enterprise 1, Rigetti Cepheus-1-36Q | 36 |
| IQM Garnet | 20 |
| AQT IBEX Q1 | 12 |

**Largest device: 107 qubits.**

**Needed for RSA-2048:** about 1,400 logical qubits and 900,000 physical qubits (Gidney, 2025) [1]. In 2019 the estimate was 20 million physical qubits [2]. A 2026 design claims under 100,000, using a different error-correcting code that needs more qubit connections [3]. All three assume a 0.1% gate error rate.

**The gap:** 900,000 ÷ 107 ≈ 8,400, about 4 orders of magnitude. A qubit count leaves out error correction: today's qubits are noisy, while the attack needs error-corrected ones running for days.

## Exposure map

Shor's algorithm breaks RSA and elliptic-curve cryptography, which utilities use to set up encrypted links and to sign data [4].

- **Remote-access VPNs:** traffic recorded today can be decrypted later ("harvest now, decrypt later").
- **Control-center-to-substation links (SCADA):** recorded data can be read later, and forged signatures could pass as real commands.
- **Firmware signing on grid devices:** a forged signature could install malicious firmware that stays on the device for years.

## Migration plan

NIST will phase out RSA and elliptic-curve cryptography after 2030 and ban them under its standards after 2035 [5]. Replacements: ML-KEM for key exchange, and ML-DSA or SLH-DSA for signatures [6].

1. **Inventory** every place RSA and elliptic-curve cryptography is used.
2. **VPNs first:** traffic is being recorded now, and the fix is a software update.
3. **Firmware signing:** a forged update is a lasting compromise.
4. **SCADA links:** switch key exchange and signatures.
5. **Symmetric keys (AES) last:** Grover's algorithm only weakens them (see Step 2b).

## Sources

1. Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits" (2025). https://arxiv.org/abs/2505.15917
2. Gidney and Ekerå, "How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits," Quantum 5, 433 (2021). https://arxiv.org/abs/1905.09749
3. Webster et al., "The Pinnacle architecture: reducing the cost of breaking RSA-2048 to 100 000 physical qubits using quantum LDPC codes" (2026). https://arxiv.org/abs/2602.11457
4. Shor, "Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer," SIAM J. Comput. 26, 1484 (1997).
5. NIST IR 8547, "Transition to Post-Quantum Cryptography Standards" (2026). https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8547.pdf
6. NIST FIPS 203, 204, and 205 (2024). https://csrc.nist.gov/projects/post-quantum-cryptography