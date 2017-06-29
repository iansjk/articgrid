# coding=utf-8
from __future__ import unicode_literals

from nltk.corpus import cmudict as raw_cmudict

from artictools.wordlists.frequency import frequency

FREQUENCY_CUTOFF = 10
CONSONANTS = ("B", "CH", "D", "DH", "F", "G", "HH", "JH", "K", "L", "M", "N", "NG", "P", "R", "S", "SH", "T", "TH", "V",
              "W", "Y", "Z", "ZH")
ARPABET_TO_IPA = {
    "AA": "ɑ",
    "AE": "æ",
    "AH1": "ʌ",
    "AH0": "ə",
    "AO": "ɔ",
    "B": "b",
    "CH": "tʃ",
    "D": "d",
    "DH": "ð",
    "EH": "ɛ",
    "ER1": "ɝ",
    "ER0": "ɚ",
    "EY": "aɪ",
    "F": "f",
    "G": "g",
    "HH": "h",
    "IH": "ɪ",
    "IY": "i",
    "JH": "dʒ",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "ŋ",
    "OW": "oʊ",
    "OY": "ɔɪ",
    "P": "p",
    "R": "ɹ",
    "S": "s",
    "SH": "ʃ",
    "T": "t",
    "TH": "θ",
    "UH": "ʊ",
    "UW": "u",
    "V": "v",
    "W": "w",
    "Y": "j",
    "Z": "z",
    "ZH": "ʒ"
}


class Entry(object):
    def __init__(self, frequency, pronunciations):
        self.frequency = frequency
        self.pronuncations = pronunciations


def num_syllables(tokens):
    count = 0
    for token in tokens:
        if token[-1].isdigit():
            count += 1
    return count


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


cmudict = raw_cmudict.dict()
wordset = cmudict.viewkeys() & {word for word in frequency.viewkeys() if frequency[word] >= FREQUENCY_CUTOFF}
words = {word: Entry(frequency[word], cmudict[word]) for word in wordset}
