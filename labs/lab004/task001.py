import utils


import random
from math import gcd


def random_odd_512_bit_number() -> int:

    n = random.getrandbits(512)

    # most bit is 512 -> length of n is 512
    n |= (1 << 511)

    # least bit is 1 -> odd
    n |= 1

    return n
def test_single_number(n: int, rounds: int = 100) -> bool:
    # n = 11449340794930455100657121819253416426590934459361534335175617393675870733666837095137122144746188233886656822933003901931311491222423625414359136922170943
    print(f"Testing n = {n}")
    print(f"bit length = {n.bit_length()}")

    if n < 2:
        print("Result: composite")
        return False

    if n in (2, 3):
        print("Result: probably prime")
        return True

    if n % 2 == 0:
        print("Result: composite")
        return False

    was_composite = False
    for i in range(1, rounds + 1):

        passed, a = utils.miller_robin(n)

        print(f"Test #{i}: a = {a}")

        if not passed:
            was_composite = True
            print("Result: composite")
            # return False
        else:
            print("Result: probably prime")
        # print("Answer: probably prime")

    if was_composite:
        return False
    else:
        print("Final result: probably prime")
        return True


def test_single_number_normal_version(n: int, rounds: int = 100) -> bool:
    n = 11449340794930455100657121819253416426590934459361534335175617393675870733666837095137122144746188233886656822933003901931311491222423625414359136922170943
    print(f"Testing n = {n}")
    print(f"bit length = {n.bit_length()}")

    if n < 2:
        print("Result: composite")
        return False

    if n in (2, 3):
        print("Result: probably prime")
        return True

    if n % 2 == 0:
        print("Result: composite")
        return False

    for i in range(1, rounds + 1):

        passed, a = utils.miller_robin(n)

        print(f"Test #{i}: a = {a}")

        if not passed:
            print("Result: composite")
            return False

        print("Answer: probably prime")


    print("Final result: probably prime")
    return True


def test_given_512_bit_numbers(numbers: list[int], rounds: int = 100) -> None:
    for index, n in enumerate(numbers, start=1):
        print("=" * 80)
        print(f"Number #{index}")

        if n.bit_length() != 512:
            print(f"Warning: this number has bit length {n.bit_length()}, not 512")

        test_single_number(n, rounds)


def test_random_512_bit_numbers(count: int = 100, rounds: int = 100) -> None:
    for index in range(1, count + 1):
        print("=" * 80)
        print(f"Random 512-bit number #{index}")

        n = random_odd_512_bit_number()

        test_single_number_normal_version(n, rounds)

if __name__ == "__main__":
    # test_random_512_bit_numbers(1, 100)
    test_random_512_bit_numbers(1)
