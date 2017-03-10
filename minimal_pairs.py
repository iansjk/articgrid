from __future__ import absolute_import, print_function
from nltk.corpus import cmudict, words

if __name__ == "__main__":
    target1 = "V"  # raw_input("First target: ")
    target2 = "SH"  # raw_input("Second target: ")
    location = "final" #  raw_input("Initial or final: ")

    subset1 = {}
    subset2 = {}
    d = cmudict.dict()
    wordlist = words.words()
    common_words = d.viewkeys() & wordlist
    for word in common_words:
        for tokens in d[word]:
            if location == "initial":
                index = 0
            elif location == "final":
                index = -1

            if tokens[index] == target1:
                subset1[word] = tokens
            elif tokens[index] == target2:
                subset2[word] = tokens

    for word1, pron1 in subset1.iteritems():
        for word2, pron2 in subset2.iteritems():
            if len(pron1) == len(pron2):
                if (location == "initial" and pron2 == [target2, ] + pron1[1:]) or (location == "final" and pron2 == pron1[:-1] + [target2, ]):
                    print("{} -- {}".format(word1, word2))

