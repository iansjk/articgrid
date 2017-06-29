import six

from artictools.wordlists.corpus import words, num_syllables


def find_by_syllable_count(count):
    results = []
    for word, entry in six.iteritems(words):
        if min([num_syllables(pron) for pron in entry.pronunciations]) == count:
            results.append(word)
    return results
