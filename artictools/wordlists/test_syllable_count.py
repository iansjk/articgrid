from unittest import TestCase

import six

from artictools.wordlists.corpus import common_cmudict, num_syllables
from artictools.wordlists.syllable_count import find_by_syllable_count


class TestSyllableCount(TestCase):
    def setUp(self):
        self.example_words = {
            1: {"egg", "bar", "eye"},
            2: {"eighty", "event", "unit"},
            3: {"syllable", "projection", "computer"},
            4: {"adorable", "assertiveness", "comprehension"},
            5: {"collaboration", "abbreviation", "appropriation"},
        }

        self.different_syllable_count_prons = [
            ("comparable", 3),  # 3 or 4
            ("handling", 2),  # 2 or 3
            ("collaborative", 4)  # 4 or 5
        ]

        self.same_syllable_count_prons = [
            ("combine", 2),  # COM-bine, com-BINE
            ("subject", 2),  # SUB-ject, sub-JECT
            ("complex", 2),  # COM-plex, com-PLEX
            ("data", 2),  # DAE-teh, DAY-tuh
        ]

    def test_num_syllables_different_counts(self):
        # for words with multiple pronunciations that have different syllable counts,
        # we expect the smallest one
        for word, expected in self.different_syllable_count_prons:
            self.assertIn(word, common_cmudict)
            self.assertTrue(any([num_syllables(pron) == expected for pron in common_cmudict[word]]))

    def test_num_syllables_same_count(self):
        for word, expected in self.same_syllable_count_prons:
            self.assertIn(word, common_cmudict)
            self.assertTrue(all([num_syllables(pron) == expected for pron in common_cmudict[word]]))

    def test_find_syllable_count_multiple_prons(self):
        for word, expected in self.different_syllable_count_prons + self.same_syllable_count_prons:
            self.assertIn(word, find_by_syllable_count(expected))

    def test_find_by_syllable_count_zero_syllables(self):
        self.assertFalse(find_by_syllable_count(0))

    def test_find_by_syllable_count_example_words(self):
        for count, words in six.iteritems(self.example_words):
            results = set(find_by_syllable_count(count))
            for word in words:
                self.assertIn(word, common_cmudict)
                self.assertIn(word, results)
