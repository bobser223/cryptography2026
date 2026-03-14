import re
import matplotlib.pyplot as plt

import utils as cl

PATH_TO_TEXT_A = "../../data/labs/lab001/textA.txt"

def wright_frequency_to_file(letters, values, file_path: str):
    with open(file_path, "w") as f:
        for letter, value in zip(letters, values):
            print(f"{letter} {value}", file=f)


def get_chars_frequency(text: str) -> dict:
    clean = cl.clean_text(text)

    frequency = {}
    for char in clean:
        frequency[char] = frequency.get(char, 0) + 1



    return frequency

def get_chars_relative_frequency(text: str):
    frequency = get_chars_frequency(text)
    total = sum(freq.values())
    for (key, value) in frequency.items():
        frequency[key] = value / total

    return frequency




if __name__ == '__main__':
    text = ""
    with open(PATH_TO_TEXT_A, "r") as f:
        text = f.read()
    freq = get_chars_relative_frequency(text)
    sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    letters = [x[0] for x in sorted_items]
    values = [x[1] for x in sorted_items]

    wright_frequency_to_file(letters, values, "../../data/labs/lab001/frequency.txt")

    plt.bar(letters, values)

    plt.xlabel("Letters")
    plt.ylabel("Relative frequency")
    plt.title("Letter frequency in text")

    plt.show()




