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
    incidents = {
        Incident.incident_id: {
            "latitude": Incident.latitude,
            "longitude": Incident.longitude,
            "address": Incident.address,
            "city": Incident.city,
            "state": Incident.state,
            "date": Incident.date,
            "time": Incident.time,
            "description": Incident.description,
            "rec_number": Incident.police_rec_num
        }
        for incident in Incident.query}

    return jsonify(incidents)







	


if __name__ == "__main__":
    app.run(debug=True)