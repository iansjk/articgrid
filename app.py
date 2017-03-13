from flask import Flask, render_template, json, request, url_for

from images.arasaac import find_images
from targets.minimal_pairs import find_minimal_pairs

app = Flask(__name__)


@app.context_processor
def inject_navigation():
    return {
        "active_page": "Home",
        "navigation": (
            ("Home", "/"),
            ("Images", url_for("images")),
            ("Minimal Pairs", url_for("minimal_pairs")),
            ("Moving Across Syllables", url_for("moving_across_syllables")),
        )}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/images/")
def images():
    return render_template("images.html")


@app.route("/images/search/<query>")
def image_search(query):
    return json.jsonify({
        "results": find_images(query),
    })


@app.route("/minimal-pairs/")
def minimal_pairs():
    return render_template("minimal-pairs.html")


@app.route("/minimal-pairs/search", methods=["POST"])
def minimal_pair_search():
    target1 = request.form["target1"]
    target2 = request.form["target2"]
    position = request.form["position"]
    return json.jsonify({
        "results": find_minimal_pairs(target1, target2, position),
    })


@app.route("/moving-across-syllables/")
def moving_across_syllables():
    return render_template("moving-across-syllables.html")


if __name__ == "__main__":
    app.run()
