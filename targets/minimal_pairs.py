from __future__ import absolute_import, print_function
from . import corpus


def find_minimal_pairs(target1, target2, location):
    subset1 = {}
    subset2 = {}
    for word, pronunciation in corpus.common_cmudict:
        if location == "initial":
            index = 0
        elif location == "final":
            index = -1

        if pronunciation[index] == target1:
            subset1[word] = pronunciation
        elif pronunciation[index] == target2:
            subset2[word] = pronunciation

    results = []
    for word1, pron1 in subset1.iteritems():
        for word2, pron2 in subset2.iteritems():
            if len(pron1) == len(pron2):
                if (location == "initial" and pron2 == [target2, ] + pron1[1:]) or \
                        (location == "final" and pron2 == pron1[:-1] + [target2, ]):
                    results.append((word1, word2))
    return results
