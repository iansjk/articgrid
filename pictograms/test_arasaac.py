from unittest import TestCase

from arasaac import find_pictograms


class TestArasaac(TestCase):
    def test_find_pictograms_empty(self):
        self.assertRaises(ValueError, find_pictograms, "")
        self.assertRaises(ValueError, find_pictograms, None)

    def test_find_pictograms_unique(self):
        result = find_pictograms("food")
        self.assertGreater(len(result), 0)
        for _, urls in result:
            self.assertEqual(len(set(urls)), len(urls))
