from flask import Flask, url_for
from flask_jsglue import JSGlue

from .wordlists.corpus import consonants, arpabet_to_ipa

STATIC_FOLDER = "static"
app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config["MINIMUM_PICTOGRAM_QUERY_LENGTH"] = 3
JSGlue(app)

from . import views


@app.context_processor
def inject_constants():
    return {
        "project_name": "ArticTools",
        "active_page": "Home",
        "navigation": (
            ("Home", "/"),
            ("Pictograms", url_for("pictograms")),
            ("Wordlists", (
                ("By Syllable Count", url_for("syllables")),
                ("By Sounds", url_for("sounds")),
                ("Minimal Pairs", url_for("minimal_pairs")),
            )),
            ("Grid Builder", url_for("grid_builder")),
            ("About", url_for("about")),
        ),
        "consonants": consonants,
        "arpabet_to_ipa": arpabet_to_ipa
    }


@app.after_request
def add_cache_header(response):
    response.cache_control.max_age = 300
    response.cache_control.public = True
    return response
