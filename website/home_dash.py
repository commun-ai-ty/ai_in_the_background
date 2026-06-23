from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash, make_response, current_app
import re
import random
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
from flask import session


home_dash = Blueprint("home_dash", __name__)

@home_dash.route("/")
def home():
    return render_template("home.html")