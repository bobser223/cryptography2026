import random
import utils


def swap_two_random_letters(text: str) -> str:
    letter_indices = [i for i, ch in enumerate(text) if ch.isalpha()]

    i, j = random.sample(letter_indices, 2)

    chars = list(text)
    chars[i], chars[j] = chars[j], chars[i]

    return "".join(chars)

def hamming_distance_bits(hex1: str, hex2: str) -> int:
    x = int(hex1, 16) ^ int(hex2, 16)
    return x.bit_count()


if __name__ == '__main__':
    pangrammas = ["Фабрикуймо гідність, лящім їжею, ґав хапаймо, з'єднавці чаш!",
                  "Юнкерський джинґл, що при безхліб'ї чує фашист, це ловця гімн.",
                  "Хвацький юшковар Філіп щодня на ґанку готує сім'ї вечерю з жаб",
                  "В Бахчисараї фельд'єґер зумів одягнути ящірці жовтий капюшон!",
                  "На подушечці форми любої є й ґудзик, щоб пір'я геть жовте сховати.",
                  "Щурячий бугай із їжаком-харцизом в'ючись підписали ґешефт у єнах.",
                  "Грішний джиґіт, що хотів у Францію, позбувався цієї думки з'їдаючи трюфель.",
                  "Десь чув, що той фраєр привіз їхньому царю грильяж та класну шубу з пір'я ґави.",
                  "Жебракують філософи при ґанку церкви в Гадячі, ще й шатро їхнє п'яне знаємо.",
                  "Протягом цієї п'ятирічки в ґрунт було висаджено гарбуз, шпинат та цілющий фенхель."]

    for pangramma in pangrammas:
        swapped = swap_two_random_letters(pangramma)
        hashed_swapped = utils.sha256_str_out(swapped)
        hashed =utils.sha256_str_out(pangramma)
        print(
            f"Original: {pangramma}\n"
            f"Swapped: {swapped}\n"
            f"Hashed: {hashed}\n"
            f"Hashed swapped: {hashed_swapped}\n"
            f"Distance: {hamming_distance_bits(hashed, hashed_swapped)}\n"
        )

