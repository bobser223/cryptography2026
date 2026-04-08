import utils

import random

# block = [
#     b0, b1, b2, b3,
#     b4, b5, b6, b7,
#     b8, b9, b10, b11,
#     b12, b13, b14, b15
# ]

# state = [
#     [b0,  b4,  b8,  b12],
#     [b1,  b5,  b9,  b13],
#     [b2,  b6,  b10, b14],
#     [b3,  b7,  b11, b15],
# ]
# state[row][col]


# -------------------- bytes <-> state --------------------

def bytes_to_state(block: list[int]) -> list[list[int]]:
    """
    16 bytes -> state[row][col]
    AES state заповнюється по стовпцях.
    """
    if len(block) != 16:
        raise ValueError("Block must contain exactly 16 bytes")

    state = [[0] * 4 for _ in range(4)]
    for col in range(4):
        for row in range(4):
            state[row][col] = block[4 * col + row]
    return state


def state_to_bytes(state: list[list[int]]) -> list[int]:
    """
    state[row][col] -> 16 bytes
    """
    block = [0] * 16
    for col in range(4):
        for row in range(4):
            block[4 * col + row] = state[row][col]
    return block


# -------------------- bit helpers --------------------




def random_bytes(n: int) -> list[int]:
    return [random.randrange(256) for _ in range(n)]


# -------------------- AES wrappers --------------------

def aes_encrypt_block(block16: list[int], key: list[int], Nk: int, Nr: int) -> list[int]:
    state = bytes_to_state(block16)
    w = utils.key_expansion(key, Nk, Nr)
    out_state = utils.cifer(state, Nr, w)
    return state_to_bytes(out_state)


def aes_decrypt_block(block16: list[int], key: list[int], Nk: int, Nr: int) -> list[int]:
    state = bytes_to_state(block16)
    w = utils.key_expansion(key, Nk, Nr)
    out_state = utils.inv_cipher(state, Nr, w)
    return state_to_bytes(out_state)


def aes128_encrypt(block16: list[int], key16: list[int]) -> list[int]:
    return aes_encrypt_block(block16, key16, Nk=4, Nr=10)


def aes192_encrypt(block16: list[int], key24: list[int]) -> list[int]:
    return aes_encrypt_block(block16, key24, Nk=6, Nr=12)


def aes256_encrypt(block16: list[int], key32: list[int]) -> list[int]:
    return aes_encrypt_block(block16, key32, Nk=8, Nr=14)

def aes128_decrypt(block16: list[int], key16: list[int]) -> list[int]:
    return aes_decrypt_block(block16, key16, Nk=4, Nr=10)

def aes192_decrypt(block16: list[int], key24: list[int]) -> list[int]:
    return aes_decrypt_block(block16, key24, Nk=6, Nr=12)

def aes256_decrypt(block16: list[int], key32: list[int]) -> list[int]:
    return aes_decrypt_block(block16, key32, Nk=8, Nr=14)

def avalanche_test_plaintext(Nk: int, Nr: int, trials: int = 100000) -> float:
    """
    Середня кількість змінених бітів у ciphertext
    при зміні 1 біта plaintext.
    """
    key_len = 4 * Nk   # bytes
    total = 0

    for _ in range(trials):
        pt = random_bytes(16)
        key = random_bytes(key_len)

        ct1 = aes_encrypt_block(pt, key, Nk, Nr)

        bit_to_flip = random.randrange(128)   # у plaintext 128 біт
        pt2 = flip_bit_in_bytes(pt, bit_to_flip)

        ct2 = aes_encrypt_block(pt2, key, Nk, Nr)

        total += hamming_distance_bytes(ct1, ct2)

    return total / trials


def avalanche_test_key(Nk: int, Nr: int, trials: int = 100000) -> float:
    """
    Середня кількість змінених бітів у ciphertext
    при зміні 1 біта key.
    """
    key_len = 4 * Nk   # bytes
    total = 0

    for _ in range(trials):
        pt = random_bytes(16)
        key = random_bytes(key_len)

        ct1 = aes_encrypt_block(pt, key, Nk, Nr)

        bit_to_flip = random.randrange(8 * key_len)
        key2 = flip_bit_in_bytes(key, bit_to_flip)

        ct2 = aes_encrypt_block(pt, key2, Nk, Nr)

        total += hamming_distance_bytes(ct1, ct2)

    return total / trials


def self_test_once(bit):

    # bit = 128

    if bit == 128:
        Nk = 4
        Nr = 10
    elif bit == 192:
        Nk = 6
        Nr = 12
    elif bit == 256:
        Nk = 8
        Nr = 14
    else:
        print("Wrong bit")
        return

    key_len = 4 * Nk
    pt = random_bytes(16)
    key = random_bytes(key_len)

    ct = aes_encrypt_block(pt, key, Nk, Nr)
    # print(f"ct={ct}")
    dec = aes_decrypt_block(ct, key, Nk, Nr)
    # print(f"dec={dec}")

    print("OK" if dec == pt else "FAIL")

def test_all():
    key_16 = random_bytes(16)
    key_24 = random_bytes(24)
    key_32 = random_bytes(32)

    block_16 = random_bytes(16)

    crypted_128 = aes128_encrypt(block_16, key_16)
    crypted_192 = aes192_encrypt(block_16, key_24)
    crypted_256 = aes256_encrypt(block_16, key_32)

    decrypted_128 = aes128_decrypt(crypted_128, key_16)
    decrypted_192 = aes192_decrypt(crypted_192, key_24)
    decrypted_256 = aes256_decrypt(crypted_256, key_32)

    if block_16 == decrypted_128 and block_16 == decrypted_192 and block_16 == decrypted_256:
        print("OK")
    else:
        print("FAIL")


if __name__ == "__main__":
    # self_test_once(128) # 128
    # self_test_once(192) # 192
    # self_test_once(256) # 256
    #
    # test_all()

    input_ = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
    key_ = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]

    print(aes128_encrypt(input_, key_))
    print(' '.join(f'{x:02x}' for x in aes128_encrypt(input_, key_)))