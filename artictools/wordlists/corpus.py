# coding=utf-8
from nltk.corpus import cmudict as raw_cmudict

from artictools.wordlists.frequency import build_frequency_dict

CUTOFF = 10
consonants = ("B", "CH", "D", "DH", "F", "G", "HH", "JH", "K", "L", "M", "N", "NG", "P", "R", "S", "SH", "T", "TH", "V",
              "W", "Y", "Z", "ZH")
arpabet_to_ipa = {
    "AA": u"ɑ",
    "AE": u"æ",
    "AH1": u"ʌ",
    "AH0": u"ə",
    "AO": u"ɔ",
    "B": u"b",
    "CH": u"t͡ʃ",
    "D": u"d",
    "DH": u"ð",
    "EH": u"ɛ",
    "ER1": u"ɝ",
    "ER0": u"ɚ",
    "EY": u"aɪ",
    "F": u"f",
    "G": u"g",
    "HH": u"h",
    "IH": u"ɪ",
    "IY": u"i",
    "JH": u"d͡ʒ",
    "K": u"k",
    "L": u"l",
    "M": u"m",
    "N": u"n",
    "NG": u"ŋ",
    "OW": u"oʊ",
    "OY": u"ɔɪ",
    "P": u"p",
    "R": u"ɹ",
    "S": u"s",
    "SH": u"ʃ",
    "T": u"t",
    "TH": u"θ",
    "UH": u"ʊ",
    "UW": u"u",
    "V": u"v",
    "W": u"w",
    "Y": u"j",
    "Z": u"z",
    "ZH": u"ʒ"
}


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
frequency = build_frequency_dict()
common_words = [word for word in cmudict if word in frequency and frequency[word] >= CUTOFF]
common_cmudict = {}
for word in common_words:
    pronunciations = [convert_schwar(pron) for pron in cmudict[word.lower()] if num_syllables(pron) > 0]
    if pronunciations:
        common_cmudict[word] = pronunciations
