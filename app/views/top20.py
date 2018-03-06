from flask import render_template
from flask_login import login_required
from app.helpers import api_get
from app import app


@app.route("/top20", methods=["GET"])
@login_required
def top20():
    query = {"filters": []}
    top20pages = api_get('top20/pages', query, True)
    top20inlinks = api_get('top20/inlinks', query, True)
    top20outlinks = api_get('top20/outlinks', query, True)
    return render_template("top20.html", top20pages=top20pages, top20inlinks=top20inlinks, top20outlinks=top20outlinks)
