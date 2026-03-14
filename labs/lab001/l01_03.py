from dbm import error

from fontTools.misc.eexec import encrypt

import utils
import l01_01 as l1
import l01_02 as l2

KEY = "шашалик"

def read_freq() -> dict:
    freq = {}
    with open("../../data/labs/lab001/frequency.txt", "r", encoding="utf-8") as f:
        for line in f:
            letter, value = line.split()
            freq[letter] = float(value)
    return freq

def count_CI_from_text(text: str) -> float:
    freq = l1.get_chars_frequency(text)
    total = sum(freq.values())

    CI = 0
    for value in freq.values():
        CI += value*(value-1)
    CI /= total*(total-1)
    return CI

def check_possible_key_length(text: str, etalon_CI: float) -> list[int]:
    candidates = []
    for key_len in range(5, 20):

        subsequences = [text[start::key_len] for start in range(key_len)]
        CIs = [count_CI_from_text(sub) for sub in subsequences if len(sub) > 1]
        avg_CI = sum(CIs) / len(CIs)
        diff = abs(avg_CI - etalon_CI)
        candidates.append((key_len, avg_CI, diff))
    candidates.sort(key=lambda x: x[2])
    return candidates

def choose_best_period(candidates, gap_ratio: float = 5.0, harmonic_tol: float = 1.2):


    if not candidates:
        return None, []

    if len(candidates) == 1:
        return candidates[0][0], candidates

    good = [candidates[0]]

    for i in range(len(candidates) - 1):
        cur_diff = candidates[i][2]
        next_diff = candidates[i + 1][2]
        gap = next_diff - cur_diff

        if cur_diff > 0 and gap / cur_diff > gap_ratio:
            break

        good.append(candidates[i + 1])

    filtered = []

    for cand in good:
        k, avg_ci, diff = cand
        is_harmonic = False

        for prev_k, prev_avg, prev_diff in filtered:
            if k % prev_k == 0 and diff <= prev_diff * harmonic_tol:
                is_harmonic = True
                break

        if not is_harmonic:
            filtered.append(cand)

    best = filtered[0][0] if filtered else good[0][0]
    return best, good

def XI_square(objected:dict, standard:dict) -> float:
    suma = 0
    for ch in utils.UA_LETTERS:
        obs = objected.get(ch, 0.0)
        exp = standard[ch]
        suma += (obs - exp) ** 2 / exp

    return suma

def get_visioner_key_by_length(text, key_len, standard_freq):
    text = utils.clean_text(text)
    subtexts = [text[start::key_len] for start in range(key_len)]
    key = ""
    for subtext in subtexts:
        candidates = []
        for i in range(len(utils.UA_LETTERS)):
            edited_subtext = [utils.idx2letter(utils.letter2idx(ch) - i) for ch in subtext]
            sub_freq = l1.get_chars_frequency("".join(edited_subtext))
            xi_score = XI_square(sub_freq, standard_freq)
            candidates.append((xi_score, i))

        key += utils.idx2letter(min(candidates)[1])

    return key

def t01():
    encrypted = ""
    with open("../../data/labs/lab001/textB.txt", "r") as f:
        text = f.read()
        encrypted = l2.visioner(text, KEY)

    with open("../../data/labs/lab001/textB_encrypted.txt", "w") as f:
        f.write(encrypted)

def t01_check():
    with open("../../data/labs/lab001/textB_encrypted.txt", "r") as f:
        encrypted = f.read()
    decrypted = l2.reverse_visioner(encrypted, KEY)
    print(decrypted)

def t02():
    with open(utils.PATH_TO_DATA + "textA.txt", "r") as f:
        textA = f.read()
        etalon_CI = count_CI_from_text(textA)
    print(etalon_CI)

    with open(utils.PATH_TO_DATA + "textB_encrypted.txt", "r") as f:
        textB_cleaned = f.read()

    candidates = check_possible_key_length(textB_cleaned, etalon_CI)
    best_period, good_candidates = choose_best_period(candidates)

    print("all:", candidates)
    print("good:", good_candidates)
    print("best:", best_period)

def t03():
    with open(utils.PATH_TO_DATA + "textA.txt", "r") as f:
        textA = f.read()
        etalon_CI = count_CI_from_text(textA)
        etalon_freq = l1.get_chars_frequency(textA)

    print(f"Etalon CI = {etalon_CI}")

    with open(utils.PATH_TO_DATA + "textB_encrypted.txt", "r") as f:
        textB_encrypted = f.read()

    candidates = check_possible_key_length(textB_encrypted, etalon_CI)
    best_period, good_candidates = choose_best_period(candidates)

    possible_keys = []

    for cand in good_candidates:
        key_len, avg_ci, diff = cand
        possible_keys.append(get_visioner_key_by_length(textB_encrypted, key_len, etalon_freq))

    CI_for_decrypted = []
    for key in possible_keys:
        decrypted = l2.reverse_visioner(textB_encrypted, key)
        CI_for_decrypted.append((abs(count_CI_from_text(decrypted) - etalon_CI), key))

    correct_key = min(CI_for_decrypted, key=lambda x: abs(x[0]))[1]

    decrypted = l2.reverse_visioner(textB_encrypted, correct_key)

    with open(utils.PATH_TO_DATA + "textB_cleaned.txt", "r") as f:
        textB_cleaned = f.read()

    error_count = 0
    for (ch1, ch2) in zip(textB_cleaned, decrypted):
        if ch1 != ch2:
            error_count += 1

    errors_per_cent = error_count / len(textB_cleaned) * 100
    if errors_per_cent == 0:
        print("No errors")
    else:
        print(f"errors per cent = {errors_per_cent}")
    print(f"correct key = {correct_key}")




if __name__ == "__main__":
    # t01()
    # t01_check()
    t03()
