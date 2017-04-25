from nltk.corpus import cmudict
from nltk.corpus import words


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


_cmudict = cmudict.dict()
common_words = words.words()
common_cmudict = {key: [convert_schwar(pron) for pron in _cmudict[key]] for key in _cmudict.viewkeys() & common_words}
