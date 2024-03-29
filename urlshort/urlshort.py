import os
import json
from werkzeug.utils import secure_filename
from flask import (Blueprint, render_template, request, redirect,
                   url_for, flash, abort, session, jsonify)

bp = Blueprint('urlshort', __name__)


@bp.route("/")
def home():
    return render_template("home.html", codes=session.keys())


@bp.route("/your-url", methods=["POST", "GET"])
def your_url():
    if request.method == "POST":
        urls = {}

        if os.path.exists("../urls.json"):
            with open("../urls.json", "rt") as f:
                urls = json.load(f)

        if request.form["code"] in urls.keys():
            flash("This code already exists, choose another one")
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form["code"]] = {"url": request.form["url"]}
        elif 'file' in request.files.keys():
            file = request.files['file']
            file_name = request.form["code"] + secure_filename(file.filename)
            urls[request.form["code"]] = {"file": file_name}
            file.save(os.getcwd() + f"/urlshort/static/files/{file_name}")
        else:
            flash("Invalid payload")
            return redirect(url_for('urlshort.home'))

        with open("../urls.json", "wt") as f:
            f.write(json.dumps(urls))
            session[request.form["code"]] = True

        return render_template("your-url.html", code=request.form["code"])
    else:
        return redirect(url_for("urlshort.home"))


@bp.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists("../urls.json"):
        with open("../urls.json", "rt") as f:
            urls = json.load(f)

        if code in urls.keys():
            if 'url' in urls[code]:
                return redirect(urls[code]['url'])
            elif 'file' in urls[code]:
                return redirect(url_for('static', filename='/files/' + urls[code]['file']))
            else:
                flash("Invalid data")
                return redirect(url_for('urlshort.home'))

    return abort(404)


@bp.route("/api")
def api():
    return jsonify(list(session.keys()))


@bp.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
