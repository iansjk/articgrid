from flask import Flask, render_template, json
from images import arasaac

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/image-search/<query>")
def image_search(query):
    return json.jsonify(arasaac.find_images(query))


if __name__ == "__main__":
    app.run()
