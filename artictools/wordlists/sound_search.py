from __future__ import absolute_import, print_function

from .corpus import common_cmudict


def find_sound_sequence(position, *targets):
    results = []
    for word, pronunciations in common_cmudict.items():
        for pronunciation in pronunciations:
            if len(pronunciation) >= len(targets):
                # ensure word is at least as long as the target sequence; this prevents weirdness like "str" initial
                # returning the word "st" (an abbreviation for "street" which does start with the "str" sequence)
                if len(word) >= len(targets) and \
                        (position == "initial" and pronunciation[:len(targets)] == list(targets)) or \
                        (position == "final" and pronunciation[-len(targets):] == list(targets)):
                    results.append(word)
                    break
    return results
