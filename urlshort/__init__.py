from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = "anslefjslnfef45y5R5yryrr5R%r5RGEFersfs$eTEGetg"

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app
