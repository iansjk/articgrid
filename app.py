from flask import Flask, render_template, json, request

from images.arasaac import find_images
from targets.minimal_pairs import find_minimal_pairs

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/image-search/<query>")
def image_search(query):
    return json.jsonify({
        "results": find_images(query),
    })


@app.route("/minimal-pair-search")
def minimal_pair_search():
    target1 = request.args.get("target1")
    target2 = request.args.get("target2")
    position = request.args.get("position")
    return json.jsonify({
        "results": find_minimal_pairs(target1, target2, position),
    })


if __name__ == "__main__":
    app.run()
