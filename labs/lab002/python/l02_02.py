import random
import l02_01


def flip_bit_in_bytes(data: list[int], bit_pos: int) -> list[int]:
    """
    bit_pos: 0..(8*len(data)-1)
    """
    out = data[:] # copy
    byte_idx = bit_pos // 8
    bit_idx = bit_pos % 8
    out[byte_idx] ^= (1 << bit_idx)
    return out


def hamming_distance_bytes(a: list[int], b: list[int]) -> int:
    if len(a) != len(b):
        raise ValueError("Lengths must match")

    dist = 0
    for x, y in zip(a, b):
        dist += (x ^ y).bit_count()
    return dist


def change_one_random_bit(bytes_: list[int]) -> list[int]:
    random_bit_pos = random.randint(0, len(bytes_) * 8 - 1)
    return flip_bit_in_bytes(bytes_, random_bit_pos)


def test_bit_change_in_text(trials: int = 100000):
    variants = [
        ("AES-128", 4, 10),
        ("AES-192", 6, 12),
        ("AES-256", 8, 14),
    ]

    for name, Nk, Nr in variants:
        total_diff = 0

        for _ in range(trials):
            bytes_ = l02_01.random_bytes(16)
            key = l02_01.random_bytes(4 * Nk)
            bytes_with_bit_changed = change_one_random_bit(bytes_)

            crypted = l02_01.aes_encrypt_block(bytes_, key, Nk, Nr)
            crypted_with_bit_changed = l02_01.aes_encrypt_block(bytes_with_bit_changed, key, Nk, Nr)

            diff = hamming_distance_bytes(crypted, crypted_with_bit_changed)
            total_diff += diff

        avg_diff = total_diff / trials
        print(f"{name}: avg diff = {avg_diff} bits (text changed)")


def test_bit_change_in_key(trials: int = 100000):
    variants = [
        ("AES-128", 4, 10),
        ("AES-192", 6, 12),
        ("AES-256", 8, 14),
    ]

    for name, Nk, Nr in variants:
        total_diff = 0

        for _ in range(trials):
            bytes_ = l02_01.random_bytes(16)
            key = l02_01.random_bytes(4 * Nk)
            key_with_bit_changed = change_one_random_bit(key)

            crypted = l02_01.aes_encrypt_block(bytes_, key, Nk, Nr)
            crypted_with_bit_changed = l02_01.aes_encrypt_block(bytes_, key_with_bit_changed, Nk, Nr)

            diff = hamming_distance_bytes(crypted, crypted_with_bit_changed)
            total_diff += diff

        avg_diff = total_diff / trials
        print(f"{name}: avg diff = {avg_diff} bits (key changed)")


if __name__ == '__main__':
    test_bit_change_in_text()
    test_bit_change_in_key()