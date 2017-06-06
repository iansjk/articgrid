from nltk.corpus import cmudict as raw_cmudict
from nltk.corpus import words

cmudict = raw_cmudict.dict()
unix_words = set(words.words())


def convert_schwar(pronunciation):
    """Replaces the Arpabet 'ER' (schwar) with the sequence 'AH R' (schwa + r)."""
    new_pronunciation = []
    for segment in pronunciation:
        if segment.startswith("ER"):
            new_pronunciation.append("AH" + segment[2])  # use same stress as the ER
            new_pronunciation.append("R")
        else:
            new_pronunciation.append(segment)
    return new_pronunciation


common_words = [word for word in unix_words if
                word.lower() in cmudict and (word.istitle() or word.title() not in unix_words)]
common_cmudict = {word: [convert_schwar(pron) for pron in cmudict[word.lower()]] for word in common_words}
