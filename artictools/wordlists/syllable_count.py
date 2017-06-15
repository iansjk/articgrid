from .corpus import common_cmudict


def num_syllables(tokens):
    count = 0
    for token in tokens:
        if token[-1].isdigit():
            count += 1
    return count


def find_by_syllable_count(count):
    results = []
    for word, pronunciations in common_cmudict.items():
        if min([num_syllables(pron) for pron in pronunciations]) == count:
            results.append(word)
    return results
