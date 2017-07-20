import codecs
import os
from io import BytesIO
from zipfile import ZipFile

import requests

import artictools

ANC_RAW_DATA_URL = "http://www.anc.org/SecondRelease/data/ANC-all-count.zip"
ANC_DATA_FILENAME = "ANC-all-count.txt"
BASE_DIR = os.path.dirname(artictools.__file__)
ANC_DATA_PATH = os.path.join(BASE_DIR, ANC_DATA_FILENAME)


def get_anc_data():
    if not os.path.isfile(ANC_DATA_PATH):
        r = requests.get(ANC_RAW_DATA_URL)
        r.raise_for_status()
        with ZipFile(BytesIO(r.content), "r") as zip:
            zip.extract(zip.namelist()[0], BASE_DIR)
    return ANC_DATA_PATH


def _is_word_excluded(word):
    return not word or word[0] == "'"


def _is_row_excluded(word, raw_count):
    return _is_word_excluded(word) or raw_count is None


frequency = {}
with codecs.open(get_anc_data(), "r", encoding="latin-1") as csvfile:
    for row in csvfile.read().splitlines():
        try:
            (word, _, __, raw_count) = row.split("\t")
        except ValueError:
            continue

        count = int(raw_count)
        if word not in frequency:
            frequency[word] = count
        else:
            frequency[word] = max(count, frequency[word])
