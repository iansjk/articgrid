from unittest import TestCase
from .corpus import convert_schwar

class TestCorpus(TestCase):
    def test_convert_schwar(self):
        tests = {
            "evaporator": ("IH0 V AE1 P ER0 EY2 T ER0", "IH0 V AE1 P AH0 R EY2 T AH0 R"),
            "exterminator": ("IH0 K S T ER1 M AH0 N EY2 T ER0", "IH0 K S T AH1 R M AH0 N EY2 T AH0 R"),
            "fern": ("F ER1 N", "F AH1 R N"),
            "fetter": ("F EH1 T ER0", "F EH1 T AH0 R")
        }
        for word in tests.keys():
            original, expected = tests[word]
            self.assertEquals(convert_schwar(original.split()), expected.split())
