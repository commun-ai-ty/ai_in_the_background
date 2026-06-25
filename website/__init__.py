from os import getenv

from flask import Flask

URL_PREFIX = getenv("URL_PREFIX", "")


def create_app():
    app = Flask(__name__, static_url_path=f"{URL_PREFIX}/static")

    from .home_dash import home_dash

    app.register_blueprint(home_dash, url_prefix=URL_PREFIX)

    return app
