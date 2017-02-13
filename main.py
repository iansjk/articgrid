from __future__ import absolute_import, print_function
from nltk.corpus import cmudict
from sequences import Sequence
from surnames import surnames

if __name__ == "__main__":
    s = Sequence(raw_input("Sequence: "))
    d = cmudict.dict()
    for word in d:
        tokens = d[word][0]
        if s.matches(tokens) and word not in surnames:
            print(word)
