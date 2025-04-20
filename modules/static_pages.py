from flask import Blueprint, render_template

static_pages = Blueprint("static_pages", __name__)

@static_pages.route("/about")
def about():
    return render_template("about.html")

@static_pages.route("/contact")
def contact():
    return render_template("contact.html")

@static_pages.route("/privacy")
def privacy():
    return render_template("privacy.html")