from numpy import character

UA_LETTERS = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
UA_LETTERS_SET = set(UA_LETTERS)

PATH_TO_DATA = "../../data/labs/lab001/"


def clean_text(text: str) -> str:
    text = text.lower()
    clean = ''.join(c for c in text.lower() if c in UA_LETTERS_SET)
    return clean

def letter2idx(letter: str) -> int:
    return UA_LETTERS.index(letter)

def idx2letter(idx: int) -> str:
    return UA_LETTERS[idx%len(UA_LETTERS)]


if __name__ == "__main__":
    input_file = "../../data/labs/lab001/textB.txt"
    output_file = "../../data/labs/lab001/textB_cleaned.txt"
    cleanedB = ""
    with open(input_file, "r") as f:
        text = f.read()
        cleanedB = clean_text(text)

    with open(output_file, "w") as f:
        f.write(cleanedB)