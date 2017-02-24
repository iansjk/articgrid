from __future__ import absolute_import, print_function
from nltk.corpus import cmudict, words
from sequences import Sequence

if __name__ == "__main__":
    s = Sequence(raw_input("Sequence: "))
    d = cmudict.dict()
    wordlist = words.words()
    results = []
    for word in d:
        # check each pronunciation, if word has alternative pronunciations
        if any([s.matches(tokens) for tokens in d[word]]) and word in wordlist:
            results.append(word)

    results.sort()
    for result in results:
        print(result)
