from unittest import TestCase

from artictools.pictograms.arasaac import find_pictograms


class TestArasaac(TestCase):
    def test_find_pictograms_unique(self):
        result = []
        page1 = find_pictograms("food", 0)
        self.assertGreater(len(page1.result), 0)
        result += page1.result
        max_pages = page1.max_pages
        for i in range(1, max_pages):
            result += find_pictograms("food", i)
        for _, pictogram_ids in result:
            self.assertEqual(len(set(pictogram_ids)), len(pictogram_ids))
