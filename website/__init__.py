from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv


URL_PREFIX = getenv("URL_PREFIX", "")


def create_app():
    app = Flask(__name__, static_url_path=f"{URL_PREFIX}/static")

    from .home_dash import home_dash

    app.register_blueprint(home_dash, url_prefix=URL_PREFIX)

    return app
