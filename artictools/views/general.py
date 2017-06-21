from flask import Blueprint, render_template, redirect

from artictools import STATIC_FOLDER

bp = Blueprint("general", __name__)


@bp.route("/")
def index():
    return render_template("general/index.html")


@bp.route("/grid-builder")
def grid_builder():
    return render_template("general/grid-builder.html")


@bp.route("/about")
def about():
    return render_template("general/about.html")


@bp.route("/%s/pictograms/<int:pictogram_id>" % STATIC_FOLDER)
def static_pictogram(pictogram_id):
    return redirect("https://images.artic.tools/pictograms/%d.png" % pictogram_id)
