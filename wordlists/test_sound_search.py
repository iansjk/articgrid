from unittest import TestCase

from .sound_search import find_sound_sequence


class TestSoundSearch(TestCase):
    TRIPLE_ONSETS = (
        ("S", "P", "L"),  # split
        ("S", "P", "R"),  # spry
        ("S", "P", "Y"),  # spew
        ("S", "T", "R"),  # strip
        ("S", "T", "Y"),  # stew
        ("S", "K", "L"),  # sclerosis
        ("S", "K", "R"),  # screen
        ("S", "K", "W"),  # squad
        ("S", "K", "Y"),  # skew
    )

    def test_triple_onsets(self):
        for triple_onset in self.TRIPLE_ONSETS:
            self.assertTrue(find_sound_sequence("initial", *triple_onset))
