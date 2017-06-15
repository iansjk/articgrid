from flask import render_template, json, request, redirect, abort

from artictools import app, STATIC_FOLDER
from artictools.pictograms.arasaac import find_pictograms
from artictools.wordlists.minimal_pairs import find_minimal_pairs
from artictools.wordlists.sound_search import find_sound_sequence


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pictograms/")
def pictograms():
    return render_template("pictograms.html")


@app.route("/pictograms/search", methods=["GET"])
def pictogram_search():
    query = request.args["query"]
    if len(query) < app.config["MINIMUM_PICTOGRAM_QUERY_LENGTH"]:
        return abort(400)

    arasaac_response = find_pictograms(request.args["query"], request.args["page"])
    return json.jsonify({
        "data": arasaac_response.result,
        "maxPages": arasaac_response.max_pages
    })


@app.route("/minimal-pairs/")
def minimal_pairs():
    return render_template("minimal-pairs.html")


@app.route("/minimal-pairs/search", methods=["GET"])
def minimal_pair_search():
    target1 = request.args["target1"]
    target2 = request.args["target2"]
    position = request.args["position"]
    return json.jsonify({
        "data": find_minimal_pairs(target1, target2, position)
    })


@app.route("/wordlists/sounds/")
def sounds():
    return render_template("sounds.html")


@app.route("/wordlists/sounds/search", methods=["GET"])
def sound_search():
    targets = request.args["targets"].split()
    position = request.args["position"]
    # the nested array is necessary for datatables to work
    return json.jsonify({
        "data": [[word] for word in find_sound_sequence(position, *targets)]
    })


@app.route("/wordlists/syllables")
def syllables():
    return render_template("syllables.html")


@app.route("/grid-builder")
def grid_builder():
    return render_template("grid-builder.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/%s/pictograms/<int:pictogram_id>" % STATIC_FOLDER)
def static_pictogram(pictogram_id):
    return redirect("https://images.artic.tools/pictograms/%d.png" % pictogram_id)
