
import l02_01
import l02_02

def test_bit_change_in_text(trials: int = 100000):

    name = "AES-128"
    Nk = 4

    for Nr in range(1, 20+1):
        total_diff = 0

        for _ in range(trials):
            bytes_ = l02_01.random_bytes(16)
            key = l02_01.random_bytes(4 * Nk)
            bytes_with_bit_changed = l02_02.change_one_random_bit(bytes_)

            crypted = l02_01.aes_encrypt_block(bytes_, key, Nk, Nr)
            crypted_with_bit_changed = l02_01.aes_encrypt_block(bytes_with_bit_changed, key, Nk, Nr)

            diff = l02_02.hamming_distance_bytes(crypted, crypted_with_bit_changed)
            total_diff += diff

        avg_diff = total_diff / trials
        print(f"{name}: avg diff = {avg_diff}, round count = {Nr} bits (text changed)")


def test_bit_change_in_key(trials: int = 100000):


    name = "AES-128"
    Nk = 4

    for Nr in range(1, 20+1):
        total_diff = 0

        for _ in range(trials):
            bytes_ = l02_01.random_bytes(16)
            key = l02_01.random_bytes(4 * Nk)
            key_with_bit_changed = l02_02.change_one_random_bit(key)

            crypted = l02_01.aes_encrypt_block(bytes_, key, Nk, Nr)
            crypted_with_bit_changed = l02_02.aes_encrypt_block(bytes_, key_with_bit_changed, Nk, Nr)

            diff = l02_02.hamming_distance_bytes(crypted, crypted_with_bit_changed)
            total_diff += diff

        avg_diff = total_diff / trials
        print(f"{name}: avg diff = {avg_diff}, round count = {Nr} bits (key changed)")

if __name__ == '__main__':
    test_bit_change_in_text()
    test_bit_change_in_key()
