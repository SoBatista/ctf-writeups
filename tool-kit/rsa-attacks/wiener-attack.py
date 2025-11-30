#!/usr/bin/env python3
from math import isqrt
from fractions import Fraction

# Funcionality
# 1. Implements Wiener’s attack on RSA (e, n)
# 2. -Recovers d, p, q if vulnerable
# 3. Decrypts the ciphertext c
# 4. Prints the plaintext (flag)

#####
# ------------------------------
# 1. INPUT: put your values here
# ------------------------------

c = 30986772272381489252970984175768553818132900398032535941949225294002655312445336821804003093788880629583179194854219042569229535283467718236891326837579786263948211914368704529501430869431427820276679426993554753287730476151596392510870531537751974257169137426976282320298662970708900668422700195962178840571
n = 62054082587237152560230015572477480050154483286657881625959417880951530941629105881863966112949307866222982543080297177265520048475782141367601470380632730334389323916722214507528508250645542674409954372208494538985825015579112229815684886921360174084163271278225301786911672369144947344421274076864472835753
e = 23196071154037196750240549941171449811079001656416143309470281203710127180188745836609906493050218107431384200381175828137551461732452063707882582684357542154639265407530692168423076840254619985638832523185956486407790622059075664946151417746876232122768812807120099960064991414762635287584709142760826191873


# --------------------------------
# 2. Continued fraction & helpers
# --------------------------------

def continued_fraction(num: int, den: int):
    """
    Compute the continued fraction expansion of num/den.
    Returns list of partial quotients [a0, a1, a2, ...].
    """
    cf = []
    while den:
        a = num // den
        cf.append(a)
        num, den = den, num - a * den
    return cf


def convergents(cf):
    """
    Generate convergents k/d from a continued fraction expansion.
    Uses the standard recurrence:
      k_i = a_i*k_{i-1} + k_{i-2}
      d_i = a_i*d_{i-1} + d_{i-2}
    """
    k_prev, k_curr = 0, 1
    d_prev, d_curr = 1, 0

    for a in cf:
        k_next = a * k_curr + k_prev
        d_next = a * d_curr + d_prev
        k_prev, k_curr = k_curr, k_next
        d_prev, d_curr = d_curr, d_next
        yield k_curr, d_curr


# -------------------------
# 3. Wiener's attack core
# -------------------------

def wiener_attack(e: int, n: int):
    """
    Try to recover d (and p,q) using Wiener's attack.
    Works when d is 'small' relative to n (classic vulnerable RSA scenario).
    Returns (d, p, q) or None if it fails.
    """
    cf = continued_fraction(e, n)

    for k, d in convergents(cf):
        if k == 0:
            continue

        # ed ≡ 1 (mod φ(n)) => ed - 1 is divisible by k
        if (e * d - 1) % k != 0:
            continue

        phi = (e * d - 1) // k

        # Now solve for p and q using:
        #   φ(n) = (p-1)(q-1) = pq - (p+q) + 1 = n - (p+q) + 1
        # => p + q = n - φ(n) + 1 = b
        b = n - phi + 1
        # Equation: x^2 - b x + n = 0
        # Discriminant: D = b^2 - 4n must be a perfect square
        D = b * b - 4 * n
        if D < 0:
            continue

        s = isqrt(D)
        if s * s != D:
            continue

        # Roots:
        p = (b + s) // 2
        q = (b - s) // 2

        if p * q == n:
            return d, p, q

    return None


# -------------------------
# 4. Decrypt & print flag
# -------------------------

def main():
    result = wiener_attack(e, n)
    if result is None:
        print("[!] Wiener's attack failed – d may not be small enough.")
        return

    d, p, q = result
    print(f"[+] Found d: {d}")
    print(f"[+] p: {p}")
    print(f"[+] q: {q}")

    # RSA decryption: m = c^d mod n
    m = pow(c, d, n)
    print(f"[+] m (int): {m}")

    # Convert integer -> bytes -> string
    m_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder="big")
    try:
        plaintext = m_bytes.decode()
    except UnicodeDecodeError:
        plaintext = repr(m_bytes)

    print(f"[+] Plaintext: {plaintext}")


if __name__ == "__main__":
    main()

