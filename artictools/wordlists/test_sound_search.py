from unittest import TestCase

import six

from artictools.wordlists.sound_search import find_sound_sequence, sequence_matches


class TestSoundSearch(TestCase):
    TRIPLE_ONSETS = {
        ("S", "P", "L"): "split",
        ("S", "P", "R"): "spring",
        ("S", "P", "Y"): "spew",
        ("S", "T", "R"): "strip",
        ("S", "T", "Y"): "stuart",
        ("S", "K", "L"): "sclerosis",
        ("S", "K", "R"): "screen",
        ("S", "K", "W"): "squad",
        ("S", "K", "Y"): "skew"
    }
    NOT_CODA = {"HH", "W", "Y"}
    R_BLENDS = {("P", "R"), ("B", "R"), ("T", "R"), ("D", "R"), ("K", "R"), ("G", "R"), ("F", "R")}
    S_BLENDS = {("S", "K"), ("S", "N"), ("S", "T"), ("S", "L"), ("S", "P"), ("S", "W"), ("S", "M")}
    L_BLENDS = {("P", "L"), ("B", "L"), ("K", "L"), ("G", "L"), ("F", "L")}

    def test_single(self):
        # NG can only be a coda
        self.assertFalse(find_sound_sequence("initial", "NG"))
        self.assertTrue(find_sound_sequence("final", "NG"))

        for not_coda in self.NOT_CODA:
            self.assertTrue(find_sound_sequence("initial", not_coda))
            self.assertFalse(find_sound_sequence("final", not_coda))

    def test_double(self):
        # make sure schwar + L words are returned
        self.assertIn("girl", find_sound_sequence("final", "R", "L"))

        # conversely make sure consonant + schwar is not
        self.assertNotIn("walker", find_sound_sequence("final", "K", "R"))

        # wildcards should match consonants only
        self.assertNotIn("tilt", find_sound_sequence("initial", "T", "*"))
        self.assertIn("trip", find_sound_sequence("initial", "T", "*"))

    def test_triple_onsets(self):
        for triple, example in six.iteritems(self.TRIPLE_ONSETS):
            result = find_sound_sequence("initial", *triple)
            self.assertIn(example, result)
            for word in result:
                self.assertGreaterEqual(len(word), 3)

    def test_medial(self):
        edh_medial_words = find_sound_sequence("medial", "DH")
        self.assertGreater(len(edh_medial_words), 0)
        self.assertIn("brother", edh_medial_words)
        self.assertNotIn("there", edh_medial_words)

        medial_st_blends = find_sound_sequence("medial", "S", "T")
        self.assertTrue(medial_st_blends)

    def test_sequence_matches(self):
        for s_blend in self.S_BLENDS:
            self.assertTrue(sequence_matches(["S", "*"], s_blend))
            self.assertTrue(sequence_matches(s_blend, ["S", "*"]))
            self.assertFalse(sequence_matches(s_blend, ["*", "S"]))
        for l_blend in self.L_BLENDS:
            self.assertTrue(sequence_matches(["*", "L"], l_blend))
            self.assertTrue(sequence_matches(l_blend, ["*", "L"]))
            self.assertFalse(sequence_matches(l_blend, ["L", "*"]))
        for r_blend in self.R_BLENDS:
            self.assertTrue(sequence_matches(["*", "R"], r_blend))
            self.assertTrue(sequence_matches(r_blend, ["*", "R"]))
            self.assertFalse(sequence_matches(r_blend, ["R", "*"]))
        for triple in self.TRIPLE_ONSETS:
            self.assertTrue(sequence_matches(["S", "*", "*"], triple))
            self.assertTrue(sequence_matches(triple, ["S", "*", "*"]))
