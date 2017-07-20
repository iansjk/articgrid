import six

from artictools.wordlists.corpus import words, CONSONANTS


def sequence_matches(sequence1, sequence2):
    return len(sequence1) == len(sequence2) and \
           all([sound1 == sound2 or (sound1 == "*" and sound2 in CONSONANTS) or \
                (sound1 in CONSONANTS and sound2 == "*") for sound1, sound2 in zip(sequence1, sequence2)])


def pronunciation_matches(pronunciation, position, targets):
    return position == "initial" and sequence_matches(pronunciation[:len(targets)], targets) or \
           position == "final" and sequence_matches(pronunciation[-len(targets):], targets) or \
           position == "medial" and sublist_in_list(targets, pronunciation[1:-1])


def sublist_in_list(sublist, full_list):
    for i in (index for index, token in enumerate(full_list) if token == sublist[0]):
        if sequence_matches(full_list[i:i + len(sublist)], list(sublist)):
            return True
    return False


def find_sound_sequence(position, *targets):
    results = []
    for word, entry in six.iteritems(words):
        for pronunciation in entry.pronunciations:
            # ensure word is at least as long as the target sequence; this prevents weirdness like "str" initial
            # returning the word "st" (an abbreviation for "street" which does start with the "str" sequence)
            if len(pronunciation) >= len(targets) and len(word) >= len(targets) and \
                    pronunciation_matches(pronunciation, position, targets):
                results.append(word)
                break
    return results
