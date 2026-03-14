
import utils as cl
from labs.lab001.utils import letter2idx


def visioner(plain_text: str, key:str):

    output = ""

    assert 5 <= len(key) <= 20

    key = cl.clean_text(key)
    clean_text = cl.clean_text(plain_text)

    i:int = 0
    for ch in clean_text:
        output += cl.idx2letter(letter2idx(ch) + letter2idx(key[i%len(key)]))

        i+=1

    return output

def reverse_visioner(ciphered_text: str, key:str):
    output = ""

    assert 5 <= len(key) <= 20

    key = cl.clean_text(key)
    clean_text = cl.clean_text(ciphered_text)

    i: int = 0
    for ch in clean_text:
        output += cl.idx2letter(letter2idx(ch) - letter2idx(key[i % len(key)]))

        i += 1

    return output




if __name__ == "__main__":
    plain_text = "добрий вечір"
    key = "калина"

    encrypted = visioner(plain_text, key)
    decrypted = reverse_visioner(encrypted, key)

    print("original :", cl.clean_text(plain_text))
    print("encrypted:", encrypted)
    print("decrypted:", decrypted)

    assert decrypted == cl.clean_text(plain_text)
    print("Тест пройдено")
