from flask import Blueprint, render_template, request, json

from artictools.wordlists.minimal_pairs import find_minimal_pairs
from artictools.wordlists.sound_search import find_sound_sequence

bp = Blueprint("wordlists", __name__, url_prefix="/wordlists")


@bp.route("/minimal-pairs/")
def minimal_pairs():
    return render_template("wordlists/minimal-pairs.html")


@bp.route("/minimal-pairs/search", methods=["GET"])
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


@bp.route("/sounds/search", methods=["GET"])
def sound_search():
    targets = request.args["targets"].split()
    position = request.args["position"]
    # the nested array is necessary for datatables to work
    return json.jsonify({
        "data": [[word] for word in find_sound_sequence(position, *targets)]
    })


@bp.route("/syllables")
def syllables():
    return render_template("wordlists/syllables.html")
