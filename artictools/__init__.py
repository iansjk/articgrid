from flask import Flask, url_for
from flask_jsglue import JSGlue

from artictools.wordlists.corpus import consonants, arpabet_to_ipa

STATIC_FOLDER = "static"
app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config["MINIMUM_PICTOGRAM_QUERY_LENGTH"] = 3
JSGlue(app)

from views import general
from views import pictograms
from views import wordlists

app.register_blueprint(general.bp)
app.register_blueprint(pictograms.bp)
app.register_blueprint(wordlists.bp)


@app.context_processor
def inject_constants():
    return {
        "project_name": "ArticTools",
        "active_page": "Home",
        "navigation": (
            ("Home", "general.index"),
            ("Pictograms", url_for("pictograms.index")),
            ("Wordlists", (
                ("By Syllable Count", url_for("wordlists.syllables")),
                ("By Sounds", url_for("wordlists.sounds")),
                ("Minimal Pairs", url_for("wordlists.minimal_pairs")),
            )),
            ("Grid Builder", url_for("general.grid_builder")),
            ("About", url_for("general.about")),
        ),
        "consonants": consonants,
        "arpabet_to_ipa": arpabet_to_ipa
    }


@app.after_request
def add_cache_header(response):
    response.cache_control.max_age = 300
    response.cache_control.public = True
    return response
