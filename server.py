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
def go_home():

	return render_template("homepage.html")

@app.route("/map")
def get_map():

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

@app.route("/register", methods=["GET"])
def register_form():
    """Registration Form."""
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_process():
    """Registration Form."""

    email_input = request.form['email_input']
    pw_input = request.form['password']
    username = request.form['username']
    fname = request.form['fname']
    lname = request.form['lname']
    about_me = request.form['about_me']


    if User.query.filter_by(email = email_input).all() != []:
        return redirect('/')       
    else:
        new_user = User(email= email_input, password=pw_input)
        db.session.add(new_user)
        db.session.commit() 

    return redirect('/')


@app.route("/login", methods=["GET"])
def log_in():

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
#    @copy_current_request_context
 #   def more_login():
    email_input = request.form['email_input']
    pw_input = request.form['pw_input']

    if User.query.filter(User.email == email_input, User.password == pw_input).all() != []:
        session['current_user'] = email_input
        print session['current_user']
        flash('You were successfully logged in')
        return redirect("/")
    else:
        flash('Your e-mail or password was incorrect! Please try again or Register.')
        return render_template("login.html")

@app.route("/logout")
def logout():
    del session['current_user']

    flash('Byyyyyye. You have been succesfully logged out!')
    return redirect ("/login")

@app.route("/forums")
def go_forums():

    return render_template("forums.html")

@app.route("/report")
def make_report():

    return render_template("forums.html")

@app.route("/profile")
def user_profile():

    return render_template("user_page.html")
	


if __name__ == "__main__":
    app.run(debug=True)