from flask import Blueprint, render_template

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
