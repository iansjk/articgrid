from nltk.corpus import cmudict
from nltk.corpus import words


def convert_schwar(pronunciation):
    """Replaces the Arpabet 'ER' (schwar) with the sequence 'AH R' (schwa + r)."""
    return pronunciation

_cmudict = cmudict.dict()
common_words = words.words()
common_cmudict = {key: [convert_schwar(pron) for pron in _cmudict[key]] for key in _cmudict.viewkeys() & common_words}
