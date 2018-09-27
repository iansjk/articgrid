from flask import Blueprint, render_template, request, json

from artictools.wordlists.corpus import frequency
from artictools.wordlists.minimal_pairs import find_minimal_pairs
from artictools.wordlists.sound_search import find_sound_sequence
from artictools.wordlists.syllable_count import find_by_syllable_count
from artictools.wordlists.moving_across_syllables import find_sequences

bp = Blueprint("wordlists", __name__, url_prefix="/wordlists")


@bp.route("/minimal-pairs/")
def minimal_pairs():
    return render_template("wordlists/minimal-pairs.html")


@bp.route("/minimal-pairs/search")
def minimal_pair_search():
    target1 = request.args["target1"]
    target2 = request.args["target2"]
    position = request.args["position"]
    return json.jsonify({
        "data": find_minimal_pairs(target1, target2, position)
    })


@bp.route("/sounds/")
def sounds():
    return render_template("wordlists/sounds.html")


@bp.route("/sounds/search")
def sound_search():
    targets = request.args["targets"].split()
    position = request.args["position"]
    return json.jsonify({
        "data": [{"word": word, "frequency": frequency[word]} for word in find_sound_sequence(position, *targets)]
    })


@bp.route("/syllables")
def syllables():
    return render_template("wordlists/syllables.html")


@bp.route("/syllables/search")
def syllable_search():
    count = int(request.args["count"])
    return json.jsonify({
        "data": [{"word": word, "frequency": frequency[word]} for word in find_by_syllable_count(count)]
    })


@bp.route("/moving-across-syllables")
def moving_across_syllables():
    return render_template("wordlists/moving-across-syllables.html")


@bp.route("/moving-across-syllables/search")
def moving_across_syllables_search():
    syllables = int(request.args["syllables"])
    return json.jsonify({
        "data": [{"word": word} for word in find_sequences(request.args["start"], request.args["end"], syllables)]
    })
