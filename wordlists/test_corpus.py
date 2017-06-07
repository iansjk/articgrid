from unittest import TestCase

from .corpus import convert_schwar, common_cmudict, unix_words, cmudict


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

    def test_common_cmudict_schwars(self):
        """Test if all schwars have been converted in common_cmudict."""
        for word in common_cmudict:
            for pronunciation in common_cmudict[word]:
                # convert_schwar is idempotent and should be a NOOP if has already been called
                self.assertEquals(pronunciation, convert_schwar(pronunciation))

    def test_common_cmudict_case_insensitive_uniqueness(self):
        """Test if words in common_cmudict are case-insensitively unique."""
        duplicates_by_case = [word for word in common_cmudict if word.istitle() and word.lower() in common_cmudict]
        self.assertFalse(duplicates_by_case)

    def test_common_cmudict_case_preserved(self):
        """Test if case is preserved for words in common_cmudict."""
        for word in unix_words:
            if word.istitle() and word.lower() in cmudict:
                self.assertIn(word, common_cmudict, "%s not found in common_cmudict" % repr(word))
                lc_word = word.lower()
                self.assertNotIn(lc_word, common_cmudict, "Lowercase word %s found in common_cmudict" % repr(lc_word))
