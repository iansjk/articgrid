from flask import Flask, render_template, json, request, url_for

from pictograms.arasaac import find_pictograms
from targets.minimal_pairs import find_minimal_pairs

application = Flask(__name__)


@application.context_processor
def inject_constants():
    return {
        "project_name": "ArticTools",
        "active_page": "Home",
        "navigation": (
            ("Home", "/"),
            ("Pictograms", url_for("pictograms")),
            ("Minimal Pairs", url_for("minimal_pairs")),
            ("About", url_for("about")),
        )}


@application.after_request
def add_cache_header(response):
    response.cache_control.max_age = 300
    response.cache_control.public = True
    return response


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/pictograms/")
def pictograms():
    return render_template("pictograms.html")


@application.route("/pictograms/search", methods=["GET"])
def pictogram_search():
    query = request.args["query"]
    return json.jsonify({
        "results": find_pictograms(query),
    })


@application.route("/minimal-pairs/")
def minimal_pairs():
    return render_template("minimal-pairs.html")


@application.route("/minimal-pairs/search", methods=["GET"])
def minimal_pair_search():
    target1 = request.args["target1"]
    target2 = request.args["target2"]
    position = request.args["position"]
    return json.jsonify({
        "results": find_minimal_pairs(target1, target2, position)
    })


@application.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    application.run()
