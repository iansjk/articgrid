from flask import Blueprint, render_template, request, abort, json

from artictools import app
from artictools.pictograms.arasaac import find_pictograms

bp = Blueprint("pictograms", __name__, url_prefix="/pictograms")


@bp.route("/")
def index():
    return render_template("pictograms/pictograms.html")


@bp.route("/search")
def search():
    query = request.args["query"]
    if len(query) < app.config["MINIMUM_PICTOGRAM_QUERY_LENGTH"]:
        return abort(400)

    arasaac_response = find_pictograms(query, request.args["page"])
    return json.jsonify({
        "data": arasaac_response.result,
        "maxPages": arasaac_response.max_pages
    })
