from __future__ import absolute_import, print_function
from .corpus import common_cmudict
import re

BILABIAL = ("P", "B", "M", "W")
ALVEOLAR = ("T", "D", "S", "Z", "N", "L")
PALATAL = ("SH", "ZH", "CH", "JH", "Y", "R")
VELAR = ("K", "G", "NG", "HH")
DENTAL = ("F", "V", "TH", "DH")
VOWEL = ("AA", "AE", "AH", "AO", "AW", "AY",
         "EH", "EY",
         "IH", "IY",
         "OW", "OY", "UH", "UW", "ER")  # n.b. ER: should be a palatal
SEQUENCE_REGEX = r"(?P<start>[BAPVD])-(?P<end>[BAPVD])(?P<syllables>\d)"
SEQUENCE_MATCHER = re.compile(SEQUENCE_REGEX)


def segment_to_regex(segment):
    format_string = r"({})"
    if segment == VOWEL:
        format_string += "\d"
    return format_string.format("|".join(segment))


class Sequence(object):
    def __init__(self, sequence_string):
        d = SEQUENCE_MATCHER.search(sequence_string).groupdict()
        self.start = d['start']
        self.end = d['end']
        self.syllables = int(d['syllables'])

        segments = []
        for s in (self.start, self.end):
            # separate non-empty syllables with vowels
            if segments:
                segments.append(VOWEL)

            if s == "B":
                segments.append(BILABIAL)
            elif s == "A":
                segments.append(ALVEOLAR)
            elif s == "P":
                segments.append(PALATAL)
            elif s == "V":
                segments.append(VELAR)
            elif s == "D":
                segments.append(DENTAL)

        regex_parts = [segment_to_regex(s) for s in segments]
        self.regex = re.compile("^" + r"\t".join(regex_parts))

    def matches(self, tokens):
        m = self.regex.search("\t".join(tokens))
        s = num_syllables(tokens)
        return m is not None and s == self.syllables


def num_syllables(tokens):
    count = 0
    for token in tokens:
        if token[-1].isdigit():
            count += 1
    return count


def search_sequences(sequence_string):
    s = Sequence(sequence_string)
    results = []
    for word, pronunciations in common_cmudict.items():
        # check each pronunciation, if word has alternative pronunciations
        if any([s.matches(tokens) for tokens in pronunciations]):
            results.append(word)
    return results
