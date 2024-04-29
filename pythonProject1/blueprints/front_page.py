from flask import Blueprint, render_template

bp = Blueprint("front_page", __name__, url_prefix="/")



@bp.route("/")
def fpage():
    return render_template("FrontPage.html")