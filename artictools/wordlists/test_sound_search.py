from unittest import TestCase

from artictools.wordlists.sound_search import find_sound_sequence


class TestSoundSearch(TestCase):
    TRIPLE_ONSETS = {
        ("S", "P", "L"): "split",
        ("S", "P", "R"): "spry",
        ("S", "P", "Y"): "spew",
        ("S", "T", "R"): "strip",
        ("S", "T", "Y"): "Stuart",
        ("S", "K", "L"): "sclerosis",
        ("S", "K", "R"): "screen",
        ("S", "K", "W"): "squad",
        ("S", "K", "Y"): "skew"
    }
    NOT_CODA = {"HH", "W", "Y"}

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

    def test_triple_onsets(self):
        for triple, example in self.TRIPLE_ONSETS.items():
            result = find_sound_sequence("initial", *triple)
            self.assertIn(example, result)
            for word in result:
                self.assertGreaterEqual(len(word), 3)

    def test_medial(self):
        edh_medial_words = find_sound_sequence("medial", "DH")
        self.assertGreater(len(edh_medial_words), 0)
        self.assertIn("brother", edh_medial_words)
        self.assertNotIn("there", edh_medial_words)
