import utils

def generate_rcon(n: int) -> list[list[int]]:
    rcon = []
    x = 0x01
    for _ in range(n):
        rcon.append([x, 0x00, 0x00, 0x00])
        x = utils.xtime(x)
    return rcon


if __name__ == "__main__":
    rcon = generate_rcon(20)

    print("Rcon = [")
    for row in rcon:
        print(f"    [{', '.join(f'0x{x:02x}' for x in row)}],")
    print("]")