from os import getenv, path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Other module code
# import website.config, website.prompting


# Single, constant URL prefix applied to every blueprint and to static files.
# All destinations (links, fetch calls) go through url_for(), so they inherit this.
URL_PREFIX = getenv("URL_PREFIX", "")


def create_app():
    app = Flask(__name__, static_url_path=f"{URL_PREFIX}/static")

    from .form_app import form_app
    from .home_dash import home_dash

    # app.register_blueprint(home_dash, url_prefix=URL_PREFIX)
    app.register_blueprint(form_app, url_prefix=URL_PREFIX)

    return app
