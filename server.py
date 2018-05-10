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

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///safework'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."

####################################################################

@app.route("/")
def get_info():

	return render_template("map_page.html")

@app.route("/incidents.json")
def get_points():
    incidents = {}
    for inc in Incident.query.all():
        lat = float(inc.latitude)
        lng = float(inc.longitude)
        print inc.latitude, inc.longitude
        incidents[inc.police_rec_num] = {
            "latitude": lat,
            "longitude": lng,
            "address": inc.address,
            "city": inc.city,
            "state": inc.state,
            "year": inc.year,
            "date": inc.date,
            "time": inc.time,
            "description": inc.description}
    return jsonify(incidents)


# @app.route("/login")
# def get_info():

#     return render_template("sign_in.html")

# @app.route("/logout")
# def get_info():

#     return render_template("map_page.html")

# @app.route("/register")
# def get_info():

#     return render_template("register.html")

# @app.route("/forums")
# def get_info():

#     return render_template("forums.html")
	


if __name__ == "__main__":
    app.run(debug=True)