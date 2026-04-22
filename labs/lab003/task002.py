import random
import string
import utils
import time


def first_k_bits(digest: list[int], k: int) -> int:
    first_word = digest[0] & 0xFFFFFFFF # 32 first bits
    return first_word >> (32 - k)


def get_random_string(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def find_collision(k: int) -> bool:
    previous = set()
    for i in range(10000000):
        candidate = get_random_string(k)
        hashed = utils.sha256(candidate)
        first_bits = first_k_bits(hashed, k)
        if first_bits in previous:
            return True
        previous.add(first_bits)

    return False #no collision


def find_collision_with_k() -> list[float]:
    avg_lst = []
    for k in range(5, 16):
        avg_time = 0
        for i in range(100):
            start = time.perf_counter()
            ok = find_collision(k)
            if not ok:
                print(f"Collision found with k={k}")
            end = time.perf_counter()
            avg_time += (end - start)
        avg_lst.append(avg_time / 100)

    return avg_lst


def print_results_table(avg_lst: list[float]) -> None:
    print("+-----+-----------------+")
    print("|  k  |  avg_time_sec   |")
    print("+-----+-----------------+")
    for k, avg_time in zip(range(5, 16), avg_lst):
        print(f"| {k:>3} | {avg_time:>15.6f} |")
    print("+-----+-----------------+")




if __name__ == "__main__":
    avg_lst = find_collision_with_k()
    print_results_table(avg_lst)