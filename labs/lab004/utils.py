import math
import random
import string


def factor(m: int) -> tuple[int, int]:
        # 2^s    zero count
    s = (m & -m).bit_length() - 1
    d = m >> s                      # dividing by 2^s
    return s, d


def miller_robin(n: int) -> tuple[bool, int|None]:

    if n == 1:
        return False, None

    if n == 2 or n == 3:
        return True, None

    s, d = factor(n-1)

    a = random.randint(2, n-1)
    x = pow(a, d, n)
    if x == 1 or x == n-1:
        return True, a

    for _ in range(s-1):
        x = pow(x, 2, n)
        if x == n-1:
            return True, a


    return False, a



def is_probably_prime(n: int, rounds: int = 100) -> bool:

    if n < 2:
        return False

    if n in (2, 3):
        return True

    if n % 2 == 0:
        return False

    for _ in range(rounds):
        passed, _ = miller_robin(n)

        if not passed:
            return False

    return True


def random_odd_number_with_bits(bits: int) -> int:

    x = random.getrandbits(bits)

    x |= (1 << (bits - 1))

    x |= 1

    return x


def generate_prime(bits: int, rounds: int = 100) -> int:
    while True:
        p = random_odd_number_with_bits(bits)

        if is_probably_prime(p, rounds):
            return p


def rsa_encrypt(m: int, e: int, n: int) -> int:
    return pow(m, e, n)


def rsa_keygen(bits = 512) -> tuple[tuple[int, int], tuple[int, int, int, int, int, int]]:
    '''
    repeat:
        p = random prime of approximately 256 bits
        q = random prime of approximately 256 bits
        n = p * q
    until p != q and bit_length(n) == 512

    e = 65537

    λ = lcm(p - 1, q - 1)

    if gcd(e, λ) != 1:
        repeat key generation

    d = e^(-1) mod λ

    dP = d mod (p - 1)
    dQ = d mod (q - 1)
    qInv = q^(-1) mod p

    public_key = (n, e)
    private_key = (p, q, dP, dQ, qInv)

    return public_key, private_key

    :param bits:
    :return:
    '''

    e = 65537

    while True:
        p = generate_prime(bits // 2)
        q = generate_prime(bits // 2)

        if p == q:
            continue

        n = p * q

        if n.bit_length() != bits:
            continue

        lam = math.lcm(p - 1, q - 1)

        if math.gcd(e, lam) != 1:
            continue

        # modular inverse: d = e^(-1) mod lambda(n)
        d = pow(e, -1, lam)

        dP = d % (p - 1)
        dQ = d % (q - 1)

        # qInv = q^(-1) mod p
        qInv = pow(q, -1, p)

        public_key = (n, e)
        private_key = (p, q, d, dP, dQ, qInv)

        return public_key, private_key


def rsa_encrypt_int(m: int, public_key: tuple[int, int]) -> int:
    n, e = public_key

    if not (0 <= m < n):
        raise ValueError("message representative out of range")

    return pow(m, e, n)

def decrypt_rsa(c: int, p: int, q: int, e: int) -> int:

    '''
        dP = e-1 mod (p-1) = d mod (p-1) = 11787 mod 136 = 91
        dQ = e-1 mod (q-1) = d mod (q-1) = 11787 mod 130 = 87
        qInv = q-1 mod p = 131-1 mod 137 = 114
        m1 = cdP mod p = 836391 mod 137 = 102
        m2 = cdQ mod q = 836387 mod 131 = 120
        h = qInv.(m1 - m2) mod p = 114.(102-120+137) mod 137 = 3 [we add in an extra p here to keep the sum positive]
        m = m2 + h.q = 120 + 3.131 = 513.
    :param c:
    :param n:
    :param e:
    :param d:
    :param p:
    :param q:
    :return:
    '''
    dP = pow(e, -1, p-1)
    dQ = pow(e, -1, q-1)
    qInv = pow(q,-1, p)
    m1 = pow(c,dP, p)
    m2 = pow(c,dQ, q)
    h = qInv*(m1-m2) % p
    m = m2 + h*q
    return m


def decrypt_rsa_usually(c, p, q, d, dP, dQ, qInv):
    m1 = pow(c, dP, p)
    m2 = pow(c, dQ, q)
    h = qInv * (m1 - m2) % p
    m = m2 + h * q
    return m


import hashlib
# from wikipedia.org/wiki/Mask_generation_function
def mgf1(seed: bytes, length: int, hash_func=hashlib.sha1) -> bytes:
    """Mask generation function."""
    hLen = hash_func().digest_size
    # https://www.ietf.org/rfc/rfc2437.txt
    # 1. If l > 2^32(hLen), output "mask too long" and stop.
    if length > (hLen << 32):
        raise ValueError("mask too long")
    # 2. Let T be the empty octet string.
    T = b""
    # 3. For counter from 0 to \lceil{l / hLen}\rceil-1, do the following:
    # Note: \lceil{l / hLen}\rceil-1 is the number of iterations needed,
    #       but it's easier to check if we have reached the desired length.
    counter = 0
    while len(T) < length:
        # a. Convert counter to an octet string C of length 4 with the primitive I2OSP: C = I2OSP (counter, 4)
        C = int.to_bytes(counter, 4, "big")
        # b. Concatenate the hash of the seed Z and C to the octet string T: T = T || Hash (Z || C)
        T += hash_func(seed + C).digest()
        counter += 1
    # 4. Output the leading l octets of T as the octet string mask.
    return T[:length]


def random_bytes(length: int) -> bytes:
    return bytes(random.randint(0, 255) for _ in range(length))



def oaep_encode(message: bytes,k: int,label: bytes = b"",hash_func=hashlib.sha1):
    h_len = hash_func().digest_size
    m_len = len(message)

    if m_len > k - 2 * h_len - 2:
        raise ValueError("message too long")
    mgf = mgf1


    # a. lHash = Hash(L)
    l_hash = hash_func(label).digest()

    # b. PS = zero octets of length k - mLen - 2hLen - 2
    ps = b"\x00" * (k - m_len - 2 * h_len - 2)

    # c. DB = lHash || PS || 0x01 || M
    db = l_hash + ps + b"\x01" + message

    # sanity check
    assert len(db) == k - h_len - 1

    # d. random seed of length hLen
    seed = random_bytes(h_len)

    # e. dbMask = MGF(seed, k - hLen - 1)
    db_mask = mgf(seed, k - h_len - 1, hash_func)

    # f. maskedDB = DB xor dbMask
    masked_db = bytes(x ^ y for x, y in zip(db, db_mask))

    # g. seedMask = MGF(maskedDB, hLen)
    seed_mask = mgf(masked_db, h_len, hash_func)

    # h. maskedSeed = seed xor seedMask
    masked_seed = bytes(x ^ y for x, y in zip(seed, seed_mask))

    # i. EM = 0x00 || maskedSeed || maskedDB
    em = b"\x00" + masked_seed + masked_db
    return em


def g_step_in_oaep_decode(db, h_len, l_hash):
    '''
    Separate DB into an octet string lHash' of length hLen, a
              (possibly empty) padding string PS consisting of octets
              with hexadecimal value 0x00, and a message M as

                 DB = lHash' || PS || 0x01 || M.
    :return:
    '''

    l_hash_prime = db[:h_len]

    if l_hash_prime != l_hash:
        raise ValueError("decryption error: lHash mismatch")

    rest = db[h_len:]

    pos = rest.find(b"\x01")

    if pos == -1:
        raise ValueError("decryption error: 0x01 separator not found")

    ps = rest[:pos]

    if any(byte != 0x00 for byte in ps):
        raise ValueError("decryption error: PS contains nonzero bytes")

    message = rest[pos + 1:]

    return message


def oaep_decode(em: bytes,k: int,label: bytes = b"",hash_func=hashlib.sha1):
    mgf = mgf1
    h_len = hash_func().digest_size

    if len(em) != k:
        raise ValueError("decryption error: encoded message has invalid length")

    if k < 2 * h_len + 2:
        raise ValueError("decryption error: k is too small")


    #a. Let lHash = Hash(L)
    l_hash = hash_func(label).digest()

    #b. Separate the em into Y||maskedSeed||maskedDB
    y = em[0:1]
    masked_seed = em[1: 1 + h_len]
    masked_db = em[1 + h_len:]

    if y != b"\x00":
        raise ValueError("decryption error: Y is nonzero")

    if len(masked_seed) != h_len:
        raise ValueError("decryption error: invalid maskedSeed length")

    if len(masked_db) != k - h_len - 1:
        raise ValueError("decryption error: invalid maskedDB length")

    #c. Let seedMask = MGF(maskedDB, hLen).
    seed_mask = mgf(masked_db, h_len, hash_func)


    #d. Let seed = maskedSeed \xor seedMask.
    seed = bytes(x ^ y for x, y in zip(masked_seed, seed_mask))

    #e.  Let dbMask = MGF(seed, k - hLen - 1).
    db_mask = mgf(seed, k - h_len - 1, hash_func)

    #Let DB = maskedDB \xor dbMask.
    db = bytes(x ^ y for x, y in zip(masked_db, db_mask))

    # g. DB = lHash' || PS || 0x01 || M
    m = g_step_in_oaep_decode(db, h_len, l_hash)
    return m

if __name__ == "__main__":
    public_key, private_key = rsa_keygen(512)

    n, e = public_key
    p, q, d, dP, dQ, qInv = private_key

    print("n.bit_length() =", n.bit_length())

    message = b"hello RSA"

    k = (n.bit_length() + 7) // 8

    em = oaep_encode(message, k)
    m = int.from_bytes(em, "big")

    c = rsa_encrypt(m, e, n)

    decrypted_m = decrypt_rsa(c, p, q, e)
    decrypted_em = decrypted_m.to_bytes(k, "big")

    decrypted_message = oaep_decode(decrypted_em, k)

    print("message =", message)
    print("decrypted =", decrypted_message)

    assert decrypted_message == message
    print("OK")




















