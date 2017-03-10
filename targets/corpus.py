import nltk.corpus.cmudict as cmudict_corpus
import nltk.corpus.words as unixwords

_cmudict = cmudict_corpus.dict()
common_words = unixwords.words()
common_cmudict = {key: _cmudict[key] for key in _cmudict.viewkeys() & common_words}
