from artictools.wordlists.corpus import common_cmudict, num_syllables


def find_by_syllable_count(count):
    results = []
    for word, pronunciations in common_cmudict.items():
        if min([num_syllables(pron) for pron in pronunciations]) == count:
            results.append(word)
    return results
