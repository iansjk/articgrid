# coding=utf-8
from __future__ import unicode_literals
from unittest import TestCase

import six

from artictools.wordlists.maximal_contrast import segments, calculate_feature_distance


class TestMaximalContrast(TestCase):
    def setUp(self):
        self.all = set(segments.keys())
        self.nasals = {"m", "n", "ŋ"}
        self.semivowels = {"j", "w"}
        self.liquids = {"l", "ɹ"}
        self.affricates = {"t͡ʃ", "d͡ʒ"}
        self.labials = {"p", "b", "f", "v", "m"}
        self.alveolars = {"t", "d", "s", "z", "n", "l", "ɹ"}
        self.palatals = {"ʃ", "ʒ", "t͡ʃ", "d͡ʒ", "j"}
        self.alveolopalatals = self.palatals - {"j"}
        self.interdentals = {"θ", "ð"}
        self.sonorants = self.nasals | self.semivowels | self.liquids
        lookup_oneway = {
            "p": "b",
            "t": "d",
            "k": "g",
            "f": "v",
            "θ": "ð",
            "s": "z",
            "ʃ": "ʒ",
            "t͡ʃ": "d͡ʒ",
        }
        lookup_T = dict((v, k) for (k, v) in six.iteritems(lookup_oneway))
        self.voice_lookup = dict(lookup_T, **lookup_oneway)

    def _test_feature_for_class(self, feature, klass):
        for plus in klass:
            self.assertIn(feature, segments[plus],
                          "%s not found for segment %s in %s" % (feature, plus, segments[plus]))
        for minus in self.all - set(klass):
            self.assertNotIn(feature, segments[minus],
                             "Unexpected %s found for segment %s in %s" % (feature, minus, segments[minus]))

    def test_sonorants_voiced(self):
        self._test_feature_for_class("sonorant", self.sonorants)
        voiced = self.sonorants | {"b", "d", "g", "v", "d͡ʒ", "z", "ʒ", "ð"}
        self._test_feature_for_class("voiced", voiced)

    def test_consonantal(self):
        non_consonants = self.semivowels | {"h"}
        consonants = self.all - non_consonants
        self._test_feature_for_class("consonantal", consonants)

    def test_continuants(self):
        continuants = self.all - self.semivowels - self.liquids - self.affricates - {"p", "b", "t", "d", "k", "g"}
        self._test_feature_for_class("continuant", continuants)

    def test_nasals(self):
        self._test_feature_for_class("nasal", self.nasals)

    def test_labials(self):
        self._test_feature_for_class("labial", self.labials)

    def test_alveolars(self):
        self._test_feature_for_class("alveolar", self.alveolars)

    def test_palatals(self):
        self._test_feature_for_class("palatal", self.palatals)

    def test_velars(self):
        velars = {"k", "g", "ŋ"}
        self._test_feature_for_class("velar", velars)

    def test_anteriors(self):
        anteriors = self.labials | self.alveolars | self.interdentals
        self._test_feature_for_class("anterior", anteriors)

    def test_coronals(self):
        coronals = self.interdentals | self.alveolars | self.alveolopalatals
        self._test_feature_for_class("coronal", coronals)

    def test_sibilants(self):
        sibilants = self.alveolopalatals | {"s", "z"}
        self._test_feature_for_class("sibilant", sibilants)

    def test_feature_distinctiveness(self):
        for segment in segments:
            for other in self.all - {segment}:
                self.assertNotEqual(segments[segment], segments[other])

    def _voicing_counterpart(self, segment):
        if segment in self.sonorants | {"h"}:
            raise ValueError("No counterpart exists")
        return self.voice_lookup[segment]

    def test_feature_distance_to_self(self):
        for segment in segments:
            self.assertEqual(calculate_feature_distance(segment, segment), 0)

    def test_feature_distance_to_voiced(self):
        for segment in segments:
            try:
                voicing_counterpart = self._voicing_counterpart(segment)
            except ValueError:
                continue
            self.assertEqual(calculate_feature_distance(segment, voicing_counterpart), 1)
