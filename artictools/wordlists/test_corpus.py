from unittest import TestCase

import six

from artictools.wordlists.corpus import convert_schwar, words


class TestCorpus(TestCase):
    def test_convert_schwar(self):
        """Test if Arpabet schwars are correctly converted into schwa-r sequences."""
        tests = {
            "evaporator": ("IH0 V AE1 P ER0 EY2 T ER0", "IH0 V AE1 P AH0 R EY2 T AH0 R"),
            "exterminator": ("IH0 K S T ER1 M AH0 N EY2 T ER0", "IH0 K S T AH1 R M AH0 N EY2 T AH0 R"),
            "fern": ("F ER1 N", "F AH1 R N"),
            "fetter": ("F EH1 T ER0", "F EH1 T AH0 R")
        }
        for word in tests.keys():
            original, expected = tests[word]
            self.assertEquals(convert_schwar(original.split()), expected.split())

    def test_words_schwars(self):
        """Test if all schwars have been converted in the words dictionary."""
        for word, entry in six.iteritems(words):
            for pronunciation in entry.pronunciations:
                # convert_schwar is idempotent and should be a NOOP if has already been called
                self.assertEquals(pronunciation, convert_schwar(pronunciation))

    def test_words_case_insensitive_uniqueness(self):
        """Test if words in the words dictionray are case-insensitively unique."""
        duplicates_by_case = [word for word in words if word.istitle() and word.lower() in words]
        self.assertFalse(duplicates_by_case)
