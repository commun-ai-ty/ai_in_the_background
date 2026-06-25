import json
import random
import re

import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

home_dash = Blueprint("home_dash", __name__)


@home_dash.route("/")
def home():
    return render_template("home.html")
