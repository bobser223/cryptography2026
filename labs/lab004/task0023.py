import utils
import math
import sympy


'''
public_key, private_key = utils.rsa_keygen(512)

    n, e = public_key
    p, q, d, dP, dQ, qInv = private_key

    is_really_rsa(p, q, n, e, d)

    print("n.bit_length() =", n.bit_length())

    message = b"hello RSA"

    k = (n.bit_length() + 7) // 8

    em = utils.oaep_encode(message, k)
    m = int.from_bytes(em, "big")

    c = utils.rsa_encrypt(m, e, n)

    decrypted_m = utils.decrypt_rsa(c, p, q, e)
    decrypted_em = decrypted_m.to_bytes(k, "big")

    decrypted_message = utils.oaep_decode(decrypted_em, k)

    print("message =", message)
    print("decrypted =", decrypted_message)

    assert decrypted_message == message
    print("OK")
    '''


def is_really_rsa(p, q, n, e, d, dP,dQ,qInv) -> None:
    print("p prime =", sympy.isprime(p))
    print("q prime =", sympy.isprime(q))
    print("p != q =", p != q)
    print("n == p*q =", n == p * q)
    print("n.bit_length() =", n.bit_length())

    lam = math.lcm(p - 1, q - 1)
    print("gcd(e, lambda) =", math.gcd(e, lam))
    print("e*d % lambda =", (e * d) % lam)

    print("dP == d % (p-1) =", dP == d % (p - 1))
    print("dQ == d % (q-1) =", dQ == d % (q - 1))
    print("q*qInv % p =", (q * qInv) % p)

def is_oaep_determined():
    public_key, private_key = utils.rsa_keygen(512)

    n, e = public_key
    p, q, d, dP, dQ, qInv = private_key

    m_raw = int.from_bytes(b"hello RSA", "big")

    c1 = utils.rsa_encrypt(m_raw, e, n)
    c2 = utils.rsa_encrypt(m_raw, e, n)

    print(c1 == c2)


def random_rsa_teat():
    public_key, private_key = utils.rsa_keygen(512)

    n, e = public_key
    p, q, d, dP, dQ, qInv = private_key

    is_really_rsa(p, q, n, e, d, dP, dQ, qInv)

    print("n.bit_length() =", n.bit_length())

    message = b"hello RSA"

    k = (n.bit_length() + 7) // 8

    em = utils.oaep_encode(message, k)
    m = int.from_bytes(em, "big")

    c = utils.rsa_encrypt(m, e, n)

    decrypted_m = utils.decrypt_rsa(c, p, q, e)
    decrypted_em = decrypted_m.to_bytes(k, "big")

    decrypted_message = utils.oaep_decode(decrypted_em, k)

    print("message =", message)
    print("decrypted =", decrypted_message)

    assert decrypted_message == message
    print("OK")


if __name__ == "__main__":


    public_key, private_key = utils.rsa_keygen(512)

    n, e = public_key
    p, q, d, dP, dQ, qInv = private_key

    m_raw = int.from_bytes(b"hello RSA", "big")

    c1 = utils.rsa_encrypt(m_raw, e, n)
    c2 = utils.rsa_encrypt(m_raw, e, n)

    print(c1 == c2)