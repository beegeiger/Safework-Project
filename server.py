"""SafeWork Server"""
import json
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

from model import Forum, Post, User, Incident, Police, Source, connect_to_db, db
import requests

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

####################################################################

@app.route("/")
def get_info():

	return render_template("map_page.html")





	


if __name__ == "__main__":
    app.run(debug=True)