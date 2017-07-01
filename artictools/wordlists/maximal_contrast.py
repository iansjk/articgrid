# coding=utf-8
from __future__ import unicode_literals

features = ("sonorant", "consonantal", "continuant", "nasal", "labial", "alveolar", "palatal", "velar", "anterior",
            "coronal", "sibilant", "voiced", "lateral")

segments = {
    "m": {"sonorant", "consonantal", "continuant", "nasal", "labial", "anterior", "voiced"},
    "n": {"sonorant", "consonantal", "continuant", "nasal", "alveolar", "coronal", "anterior", "voiced"},
    "ŋ": {"sonorant", "consonantal", "continuant", "nasal", "velar", "voiced"},
    "p": {"consonantal", "labial", "anterior"},
    "b": {"consonantal", "labial", "anterior", "voiced"},
    "t": {"consonantal", "alveolar", "anterior", "coronal"},
    "d": {"consonantal", "alveolar", "anterior", "coronal", "voiced"},
    "k": {"consonantal", "velar"},
    "g": {"consonantal", "velar", "voiced"},
    "tʃ": {"consonantal", "palatal", "coronal", "sibilant"},
    "dʒ": {"consonantal", "palatal", "coronal", "sibilant", "voiced"},
    "s": {"consonantal", "continuant", "alveolar", "anterior", "coronal", "sibilant"},
    "z": {"consonantal", "continuant", "alveolar", "anterior", "coronal", "sibilant", "voiced"},
    "ʃ": {"consonantal", "continuant", "palatal", "coronal", "sibilant"},
    "ʒ": {"consonantal", "continuant", "palatal", "coronal", "sibilant", "voiced"},
    "f": {"consonantal", "continuant", "anterior", "labial"},
    "v": {"consonantal", "continuant", "anterior", "labial", "voiced"},
    "θ": {"consonantal", "continuant", "anterior", "coronal"},
    "ð": {"consonantal", "continuant", "anterior", "coronal", "voiced"},
    "l": {"sonorant", "consonantal", "alveolar", "coronal", "voiced", "anterior", "lateral"},
    "ɹ": {"sonorant", "consonantal", "alveolar", "coronal", "voiced", "anterior"},
    "j": {"sonorant", "palatal", "voiced"},
    "w": {"sonorant", "voiced"},
    "h": {"continuant"}
}


def calculate_feature_distance(s1, s2):
    dist = 0
    for feature in features:
        if (feature in segments[s1] and feature not in segments[s2]) or (
                        feature not in segments[s1] and feature in segments[s2]):
            dist += 1
    return dist


def calculate_feature_distances(s):
    distances = {}
    for segment in set(segments.keys()) - {s}:
        distances[segment] = calculate_feature_distance(s, segment)
    return distances
