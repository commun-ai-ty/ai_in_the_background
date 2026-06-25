from flask import Blueprint, render_template

home_dash = Blueprint("home_dash", __name__)


@home_dash.route("/")
def home():
    return render_template("home.html")
