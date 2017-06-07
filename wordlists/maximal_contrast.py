# coding=utf-8

features = ("sonorant", "consonantal", "continuant", "nasal", "labial", "alveolar", "palatal", "velar", "anterior",
            "coronal", "sibilant", "voiced", "lateral")

segments = {
    u"m": {"sonorant", "consonantal", "continuant", "nasal", "labial", "anterior", "voiced"},
    u"n": {"sonorant", "consonantal", "continuant", "nasal", "alveolar", "coronal", "anterior", "voiced"},
    u"ŋ": {"sonorant", "consonantal", "continuant", "nasal", "velar", "voiced"},
    u"p": {"consonantal", "labial", "anterior"},
    u"b": {"consonantal", "labial", "anterior", "voiced"},
    u"t": {"consonantal", "alveolar", "anterior", "coronal"},
    u"d": {"consonantal", "alveolar", "anterior", "coronal", "voiced"},
    u"k": {"consonantal", "velar"},
    u"g": {"consonantal", "velar", "voiced"},
    u"t͡ʃ": {"consonantal", "palatal", "coronal", "sibilant"},
    u"d͡ʒ": {"consonantal", "palatal", "coronal", "sibilant", "voiced"},
    u"s": {"consonantal", "continuant", "alveolar", "anterior", "coronal", "sibilant"},
    u"z": {"consonantal", "continuant", "alveolar", "anterior", "coronal", "sibilant", "voiced"},
    u"ʃ": {"consonantal", "continuant", "palatal", "coronal", "sibilant"},
    u"ʒ": {"consonantal", "continuant", "palatal", "coronal", "sibilant", "voiced"},
    u"f": {"consonantal", "continuant", "anterior", "labial"},
    u"v": {"consonantal", "continuant", "anterior", "labial", "voiced"},
    u"θ": {"consonantal", "continuant", "anterior", "coronal"},
    u"ð": {"consonantal", "continuant", "anterior", "coronal", "voiced"},
    u"l": {"sonorant", "consonantal", "alveolar", "coronal", "voiced", "anterior", "lateral"},
    u"ɹ": {"sonorant", "consonantal", "alveolar", "coronal", "voiced", "anterior"},
    u"j": {"sonorant", "palatal", "voiced"},
    u"w": {"sonorant", "voiced"},
    u"h": {"continuant"}
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
