from __future__ import absolute_import, print_function

import six

from artictools.wordlists.corpus import words


def sublist_in_list(sublist, full_list):
    for i in (index for index, token in enumerate(full_list) if token == sublist[0]):
        if full_list[i:i + len(sublist)] == list(sublist):
            return True
    return False


def find_sound_sequence(position, *targets):
    results = []
    for word, entry in six.iteritems(words):
        for pronunciation in entry.pronunciations:
            # ensure word is at least as long as the target sequence; this prevents weirdness like "str" initial
            # returning the word "st" (an abbreviation for "street" which does start with the "str" sequence)
            if len(pronunciation) >= len(targets) and len(word) >= len(targets):
                if position == "initial" and pronunciation[:len(targets)] == list(targets) or \
                                        position == "final" and pronunciation[-len(targets):] == list(targets) or \
                                        position == "medial" and sublist_in_list(targets, pronunciation[1:-1]):
                    results.append(word)
                    break
    return results
