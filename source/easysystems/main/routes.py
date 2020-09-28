from flask import Blueprint, render_template


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('main/home.html', title="Home")


@main.route("/about")
def about():
    return render_template('main/about.html', title="About")
