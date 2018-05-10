"""SafeWork Server"""
import json
from jinja2 import StrictUndefined


from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import (SQLAlchemy, update)

from model import Forum, Post, User, Incident, Police, Source, connect_to_db, db
import requests

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

db = SQLAlchemy()

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
        new_user = User(email= email_input, password=pw_input, username=username, fname=fname, lname=lname, description=about_me)
        db.session.add(new_user)
        db.session.commit() 

    return redirect('/')


@app.route("/login", methods=["GET"])
def log_in():
    if 'current_user' in session.keys():
        return redirect("/")
    else:
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

@app.route("/report", methods=["GET"])
def report_page():
    if 'current_user' in session.keys():
        return render_template("report_form.html")
    else:
        return redirect("/login")

@app.route("/report", methods=["POST"])
def submit_form():


    user_id = (User.query.filter(User.email == session['current_user']).first()).user_id
    inc_type = request.form['inc_type']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    lat = str(request.form['lat'])
    lng = str(request.form['lng'])
    date = request.form['date']
    time = str(request.form['time'])
    description = request.form['description']
    p_name = request.form['p_name']
    badge = request.form['badge']
    p_description = request.form['p_description']
    sting = request.form['sting']
    avoid = request.form['avoid']
    other = request.form['other']
    year = int(row["date"][0:4])

    new_report = Incident(year=year, user_id=user_id, police_dept_id=3, source_id=3, inc_type=inc_type, address=address, city=city, state=state, latitude=lat, longitude=lng, date=date, time=time, description=description, cop_name=p_name, cop_badge=badge, cop_desc=p_description, sting_strat=sting, avoidance=avoid, other=other)
    db.session.add(new_report)
    db.session.commit()

    flash('Your report has been filed and should be added to the map soon!')
    return redirect("/")

@app.route("/profile")
def user_profile():
    user = User.query.filter_by(email=session['current_user']).one()

    return render_template("user_page.html", email=user.email, username=user.username, fname=user.fname, lname=user.lname, about_me=user.description)

@app.route("/edit_profile", methods=["GET"])
def user_profile():
    user = User.query.filter_by(email=session['current_user']).one()

    return render_template("edit_profile.html", email=user.email, username=user.username, fname=user.fname, lname=user.lname, about_me=user.description)

@app.route("/edit_profile", methods=["POST"])
def user_profile():
    user = User.query.filter_by(email=session['current_user']).one()

    return render_template("user_page.html", email=user.email, username=user.username, fname=user.fname, lname=user.lname, about_me=user.description)



if __name__ == "__main__":
    app.run(debug=True)