from nltk.corpus import cmudict
from nltk.corpus import words

_cmudict = cmudict.dict()
common_words = words.words()
common_cmudict = {key: _cmudict[key] for key in _cmudict.viewkeys() & common_words}
