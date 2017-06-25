import csv
import os
import six
from io import BytesIO
from zipfile import ZipFile

import requests

import artictools

ANC_FIELDNAMES = ("word", "lemma", "pos", "count")
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


def _is_row_excluded(row):
    return _is_word_excluded(row["word"]) or row["count"] is None


def build_frequency_dict():
    frequency = {}
    with open(get_anc_data(), "r") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=ANC_FIELDNAMES, delimiter="\t")
        for row in reader:
            if _is_row_excluded(row):
                continue

            word, count = row["word"], int(row["count"])
            if word not in frequency:
                frequency[word] = count
            else:
                frequency[word] = max(count, frequency[word])

        # for cases where derived forms (-ing, -ed) are rare but base forms are common,
        # use the base form as the frequency. this means "said" and "say" will be considered equally common
        csvfile.seek(0)
        for row in reader:
            if _is_row_excluded(row):
                continue
            word, lemma = row["word"], row["lemma"]
            if word in frequency and lemma in frequency and frequency[word] < frequency[lemma]:
                frequency[word] = frequency[lemma]

    return frequency
