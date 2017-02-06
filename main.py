from __future__ import absolute_import, print_function
from nltk.corpus import cmudict
from sequences import Sequence

if __name__ == "__main__":
    s = Sequence(raw_input("Sequence: "))
    d = cmudict.dict()
    for word in d:
        tokens = d[word][0]
        if s.matches(tokens):
            print(word)
