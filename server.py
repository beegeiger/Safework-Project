"""SafeWork Server"""

from __future__ import absolute_import
from send_alerts import send_message, send_email
import flask
import bcrypt
import bcrypt
import math
import time
import json
import random
import string
import datetime
import threading
import secrets
from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
# from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (update, asc, desc)
from model import Forum, Post, User, Incident, Police, Source, Like, Flag, Contact, AlertSet, Alert, CheckIn, ReqCheck, connect_to_db, db, app
import requests
# from secrets_env import CLIENT_ID
import logging



db.init_app(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Causes error messages for undefined variables in jinja
app.jinja_env.undefined = StrictUndefined

#################################################################

level = logging.DEBUG
format = '%(asctime)s %(levelname)s %(message)s'
handlers = [logging.FileHandler('log2.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)


####################################################################

def check_in(user_id, notes):
    """Helper-function used to log a new check-in from any source"""

    #Date, time, and datetime objects are initiated for convenience
    time = datetime.datetime.now().time()
    date = (datetime.datetime.today())
    datetim = datetime.datetime.now()

    #A new check-in object is created, added, and commited
    new_check = CheckIn(user_id=user_id, notes=notes, time=time, date=date, datetime=datetim)
    db.session.add(new_check)
    db.session.commit()
    
    #All active alerts for the user are queried
    alerts = Alert.query.filter(Alert.user_id == user_id, Alert.active == True).all()
    
    #The alerts are looped through and all alerts within an hour are marked as checked-in
    for alert in alerts:
        if alert.datetime - datetim < datetime.timedelta(hours=1.5):
            if alert.interval:
                print("Alert:")
                print(alert)
                (db.session.query(Alert).filter_by(alert_id=alert.alert_id)).update(
                {'datetime': (alert.datetime + datetime.timedelta(minutes=alert.interval)), 'checked_in': True})
                db.session.query(AlertSet).filter_by(alert_set_id=alert.alert_set_id).update({'checked_in': True})
            else:
                (db.session.query(Alert).filter_by(alert_id=alert.alert_id)).update(
                {'datetime': (alert.datetime + datetime.timedelta(days=1)), 'checked_in': True})
                db.session.query(AlertSet).filter_by(alert_set_id=alert.alert_set_id).update({'checked_in': True})
    db.session.commit()
    return "Check In has been Logged!"


def create_alert(alert_id):
    """Helper Function for creating an alert's actual message body"""

    #Datetime object for now created for convenience
    datetim = datetime.datetime.now()

    #The alert in question, the user, the alert set, all other associated alerts, and the recent check-ins are all queried
    alert = Alert.query.filter_by(alert_id=alert_id).one()
    user = User.query.filter_by(user_id=alert.user_id).one()
    alert_set = AlertSet.query.filter_by(alert_set_id=alert.alert_set_id).one()
    all_alerts = Alert.query.filter(alert.alert_set_id == alert.alert_set_id, alert.datetime > alert_set.start_datetime).all()
    check_ins = CheckIn.query.filter(checkin.user_id == user.user_id, abs(checkin.datetime - datetim) <  datetime.timedelta(days=1)).all()
    
    #An empty dictionary is created to store the associated events for the alert
    events = {}
    
    #A new string that will begin the alert message is created
    message_body = """This is a Safety Alert sent by {} {} through the SafeWork Project SafeWalk Alert system,
            found at safeworkproject.org \n \n""".format(user.fname, user.lname)
    
    #If there are notes on the alert set, they are added to the message
    if alert_set.notes:
        message_body += """The user has included the following messages when they made this alert and checked in \n \n {}""".format(alert_set.message)
    
    #For all associated alerts, if there is a message longer than 2 characters, the alert is added to the events dictionary
    for a_a in all_alerts:
        if len(a_a.message) > 2:
            events[a_a.datetime] = a_a
    
    #All check-ins are added to the events dictionary
    for chks in check_ins:
        events[chks.datetime] = chks

    #Loops through all of the ordered events in the dictionary
    for key in sorted(events.keys()):
        #If the event was a scheduled alarm
        if type(events[key]) == model.Alarm:
            #Different messages are added depending on whether the alarm was check-in for and if it had a message
            if events[key].checked_in == True:
                message_body += "An alarm was scheduled for {} which {} checked-in for.".format(key, user.fname)
                if events[key].message:
                    message_body += "The Alarm included the following notes: {} \n \n".format(events[key].message)
                else:
                    message_body += "\n \n"
            else:
                message_body += "An alarm was scheduled for {} which {} MISSED the checked-in for.".format(key, user.fname)
                if events[key].message:
                    message_body += "The Alarm included the following notes: {} \n \n".format(events[key].message)
                else:
                    message_body += "\n \n"
        #If it isn't an alarm, it's a check-in object which is then added to the main message body
        else:
            message_body += "{} checked in with the app at {} and included the following message: {}".format(user.fname, key, events[key].notes)
    
    #Different messages are added depending on how many contacts are sent the alert
    if alert.contact_id3:
        message_body += """Two other contacts have been sent this alert. If you know who it might be,
                        consider reaching out and co-ordinating your effort to help {}.""".format(user.fname)
    elif alert.contact_id2:
        message_body += """One other contact has been sent this alert. If you know who it might be,
                        consider reaching out and co-ordinating your effort to help {}.""".format(user.fname)
    else:
        message_body += """You were the only person sent this alert, so if anything can be done
                        to help {}, it is up to you! Good luck!!!""".format(user.fname)
    
    #The complete message body is then returned
    return message_body

def send_alert_contacts(alert_id, message_body):
    """Helper Function that actually sends the alerts over e-mail and sms"""
    
    #The current alert and user is queried
    alert = Alert.query.filter_by(alert_id=alert_id).one()
    user = User.query.filter_by(user_id=alert.user_id).one()
    

    #An empty list is created and then filled with the contact objects associated with the alert
    contacts = []
    contacts += Contact.query.filter_by(contact_id=alert.contact_id1)
    if alert.contact_id2:
        contacts += Contact.query.filter_by(contact_id=alert.contact_id2)
    if alert.contact_id2:
        contacts += Contact.query.filter_by(contact_id=alert.contact_id3)
    
    #For each contact, an optional personal message is added to the message_body and is sent to email and sms
    for con in contacts:
        if con.c_message:
            body = con.c_message + message_body
        if con.email:
            send_email(con.email, body)
        if con.phone:
            send_sms(con.phone, body)
    return "Message Sent"

def send_alert_user(alert_id, message_body):
    """Helper Function that actually sends the alerts over e-mail and sms"""
    
    #The current alert and user is queried
    alert = Alert.query.filter_by(alert_id=alert_id).one()
    user = User.query.filter_by(user_id=alert.user_id).one()
    
    if user.email2:
        send_email(user.email2, message_body)
        print('Sending to email2')
    elif user.email:
        send_email(user.email, message_body)
        print('Sending to email1')
    if user.phone:
        send_message(user.phone, message_body)
        print('Sending to phone')
    return "Messages Sent"



def check_alerts():
    """A Helper function to run every minute to check if any alerts need to be sent"""
    
    print("Checking For Alerts and Reminders Now")

    #Datetime object for now created for convenience
    datetim = datetime.datetime.now()
    yester = datetim - datetime.timedelta(days=1)

    with app.app_context():
        #All currently-active alerts are queried 
        alerts = Alert.query.filter_by(active=True).all()
        print(alerts)
        #If at least one alert is active, the alerts are looped through to see if any need to be sent
        if len(alerts) > 0:
            for alert in alerts:
                #A new variable 'difference' is set to the timedelt between the alert and the current time
                difference = alert.datetime - datetime.datetime.now()
                
                #All recent check-ins are queried and a new counter variable checks is set to 0
                check_ins = CheckIn.query.filter(CheckIn.user_id == alert.user_id, CheckIn.datetime  >=  yester).all()
                checks = 0
                
                #For each check-in, if it is within 90 minutes before the current time, the checks counter is added by 1
                for ch in check_ins:
                    dif = datetime.datetime.now() - alert.datetime
                    if dif <= datetime.timedelta(hours=1.5) and difference > datetime.timedelta(seconds=0):
                        checks += 1
                
                #If there is no check-in and the alert is within a minute, an alert is sent
                if abs(difference) <= datetime.timedelta(minutes=1) and abs(difference) > datetime.timedelta(seconds=0) and checks == 0 and alert.sent == False:
                    print('A CHECK-IN WAS MISSED AND AN ALERT IS BEING SENT NOW!')
                    message_body = create_alert(alert.alert_id)
                    send_alert_contacts(alert.alert_id, message_body)
                    #The alert object is updates to be marked sent and inactive and its commited
                    (db.session.query(Alert).filter_by(alert_id=alert.alert_id)).update({'sent': True, 'active': False})
                    (db.session.query(AlertSet).filter_by(alert_set_id=alert.alert_set_id)).update({'active': False})
                    db.session.commit()
                
                elif abs(difference) <= datetime.timedelta(minutes=1) and abs(difference) > datetime.timedelta(seconds=0) and checks < 0 and alert.sent == False:
                    db.session.query(AlertSet).filter_by(alert_set_id=alert.alert_set_id).update({'checked_in': False})


                #If there is no check in and it is 15 minutes before an alert, a reminder message is sent
                elif abs(difference) <= datetime.timedelta(minutes=15) and abs(difference) > datetime.timedelta(minutes=14) and checks == 0 and alert.sent == False:
                    print('A CHECK-IN REMINDER IS BEING SENT NOW!')
                    message_body = """Reminder! You have a Check-In Scheduled in 15 minutes. If you don't check-in
                    by responding to this text, emailing 'safe@safeworkproject.org', or checking in on the site at
                    'www.safeworkproject.org/check_ins', your pre-set alerts will be sent to your contact(s)!"""
                    send_alert_user(alert.alert_id, message_body)
    return

#################################################################

#below is modified code from https://networklore.com/start-task-with-flask/
#Decorator which registers a function to run before the first request to the app
@app.before_first_request
def activate_job():
    """Function that runs a thread that checks for alerts every 60 seconds"""
    def run_job():
        """Function that checks for alerts and sleeps"""
        while True:
            check_alerts()
            time.sleep(60)
    #A new thread is set to run the run_job() function and is started
    thread = threading.Thread(target=run_job)
    thread.start()

def start_runner():
    """Function runs when server starts to start thread to automatically self-visit/request the site so the activate_job() function can run"""
    def start_loop():
        """Function that actually sends request to server to kickstart the 'activate_job()' funcion"""
        not_started = True
        while not_started:
            print('In start loop')
            try:
                #A new GET request is sent to the server
                r = requests.get('https://safeworkproject.org/')
                #If it is successful, it quits the start_loop() function by setting not_started to False
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
                #If the request is unsuccessful, it waits 2 seconds and tries again
            except:
                print('Server not yet started')
            time.sleep(2)
    
    #A new thread that runs start_loop() is created and started
    thread = threading.Thread(target=start_loop)
    thread.start()
    print('Started runner')

#######################################################################

@app.route("/")
def go_home():
    """Renders the safework homepage. (Tested)"""
    return render_template("homepage.html")


@app.route("/map")
def get_map():
    """Renders safework's arrest map. (Tested)"""
    return render_template("map_page.html")


@app.route("/incidents.json")
def get_points():
    """Gets the incident/marker points as JSON to be plotted on the map."""

    #Initializes empty dictionary which is then filled with the marker data
    incidents = {}
    ind = 0
    for inc in Incident.query.all():
        ind += 1
        lat = float(inc.latitude)
        lng = float(inc.longitude)
        incidents[ind] = {
            "latitude": lat,
            "longitude": lng,
            "address": inc.address,
            "city": inc.city,
            "state": inc.state,
            "year": inc.year,
            "date": inc.date,
            "time": inc.time,
            "description": inc.description,
            "source_id": inc.source_id,
            "incident_id": inc.incident_id,
            "rec_number": inc.police_rec_num}

    #The marker dictionary is jsonified and sent to the google maps API through JavaScript
    return jsonify(incidents)



@app.route("/register", methods=["GET"])
def register_form():
    """Goes to registration Form. (Tested)"""

    """Creating empty strings to send through jinja so that if someone is redirected
     from /register(POST), their data will still be in the registration form"""
    email_input = ""
    username = ""
    fname = ""
    lname = ""
    about_me = ""

    #Renders registration page with empty form variables
    return render_template("register.html", email=email_input, username=username,
                           fname=fname, lname=lname, about_me=about_me)


@app.route("/register", methods=["POST"])
def register_process():
    """Registration Form. (Tested)"""

    """Creating empty strings in case there aren't already
                data being passed from the registration redirect"""
    fname = ""
    lname = ""
    about_me = ""
    tagline = ""
    location = ""

    #Sets variables equal to the form values
    email_input = request.form['email_input']
    email2 = request.form['email_input2']
    phone = request.form['phone']

    pw_input = request.form['password']
    password2 = request.form['password2']

    username = request.form['username']
    tagline = request.form['tagline']
    location = request.form['location']
    p_word = bytes(pw_input, 'utf-8')
    hashed_word = bcrypt.hashpw(p_word, bcrypt.gensalt()).decode('utf-8')

    #These two categories need to be worked out better
    # user_type = request.form['user_type']
    # second_type = request.form['2nd']
    
    timezone = request.form['timezone']


    if pw_input != password2:
        flash("Your passwords don't match!")
        return render_template("register.html", email=email_input, username=username, fname=fname,
                               lname=lname, about_me=about_me)
    
    """Checks to make sure values exist in the optional fields
                before setting the variables equal to the form values"""
    if len(request.form['fname']) >= 1:
        fname = request.form['fname']
    if len(request.form['lname']) >= 1:
        lname = request.form['lname']
    if len(request.form['about_me']) >= 1:
        about_me = request.form['about_me']

    #Checking that the e-mail address field at least includes a "." and a "@"
    if "." not in email_input or "@" not in email_input:
        print("Testing3")
        flash(email_input + " is not a valid e-mail address!")
        return render_template("register.html", email=email_input, username=username,
                               fname=fname, lname=lname, about_me=about_me)

    #Checking that the e-mail address hasn't already been registered
    elif User.query.filter_by(email=email_input).all() != []:
        print("Testing4")
        flash(email_input + """This e-mail has already been registered! Either sign in with it,
                use a different e-mail address, or reset your password if you forgot it.""")
        return render_template("register.html", email=email_input, username=username, fname=fname,
                               lname=lname, about_me=about_me)

    #Checking that the username is available
    elif User.query.filter_by(username=username).all() != []:
        print("Testing5")
        flash(email_input + "This username is already in use! Please try another one!")
        return render_template("register.html", email=email_input, username=username, fname=fname,
                               lname=lname, about_me=about_me)

    #Checking that the password length is at least 6
    elif len(pw_input) < 6:
        print("Testing6")
        flash("Your password must be at least 5 characters long! Try again.")
        return render_template("register.html", email=email_input, username=username, fname=fname,
                               lname=lname, about_me=about_me)

    #Otherwise, the new user's information is added to the database
    else:
        print("Testing7")
        new_user = User(email=email_input, password=hashed_word, username=username, fname=fname,
                        lname=lname, description=about_me, tagline=tagline, location=location,
                        email2=email2, phone=phone, timezone=timezone)
        db.session.add(new_user)
        db.session.commit()
    print("Testing1")
    return redirect('/login')


@app.route("/login", methods=["GET"])
def log_in():
    """Render's the log-in page if user not in session,
     otherwise redirects to the homepage (Tested)"""

    if 'current_user' in list(session.keys()):
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    """Gets login info, verifies it, & either redirects to the forums or
    gives an error message (Tested)"""

    #Sets variable equal to the login form inputs
    email_input = request.form['email_input']
    pw_input = request.form['pw_input']
    user_query = User.query.filter(User.email == email_input).all()

    if user_query == []:
        flash('There is no record of your e-mail address! Please try again or Register.')
        print("No Record")
        return render_template("login.html")


    #Queries to see if the email and pword match the database. If so, redirects to the safewalk page.
    else:
        p_word = user_query[0].password
        if isinstance(pw_input, str):
            pw_input = bytes(pw_input, 'utf-8')
        passwd = bytes(p_word, 'utf-8')


        if bcrypt.hashpw(pw_input, passwd) == passwd:
            session['current_user'] = email_input
            flash('You were successfully logged in')
            return redirect("/sw_main")

        #Otherwise, it re-renders the page and throws an error message to the user
        else:
            flash('Your e-mail or password was incorrect! Please try again or Register.')
            return render_template("login.html")


@app.route("/logout")
def logout():
    """Logs user out and deletes them from the session (Tested)"""

    del session['current_user']

    flash('Bye! You have been succesfully logged out!')
    return redirect("/login")


@app.route("/forums")
def go_forums():
    """Renders the central forum page (Tested)"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    sugar = Forum.query.filter_by(forum_id=7).one()
    other = Forum.query.filter_by(forum_id=8).one()

    #Creates lists for all of the children forums of the main 8 forums
    cam_query = Forum.query.filter_by(parent_forum_id=1).all()
    dom_query = Forum.query.filter_by(parent_forum_id=2).all()
    escort_query = Forum.query.filter_by(parent_forum_id=3).all()
    porn_query = Forum.query.filter_by(parent_forum_id=4).all()
    dance_query = Forum.query.filter_by(parent_forum_id=5).all()
    phone_query = Forum.query.filter_by(parent_forum_id=6).all()
    sugar_query = Forum.query.filter_by(parent_forum_id=7).all()
    other_query = Forum.query.filter_by(parent_forum_id=8).all()

    # group_forums = Forum.query.group_by(Forum.parent_forum_id).all()

    # """Creates a list of dictionaries, each of which has all 8 forum_ids as keys with corresponding
    # children forums (or a blank string if there are no more children of a parent forum) which
    # can then be iterated through"""
    # all_forums = []
    # while (cam_query + dom_query + escort_query + porn_query +
    #        dance_query + phone_query + sugar_query + other_query) != []:
    #     row = {}
    #     if cam_query == []:
    #         row[1] = {"forum_id": "", "forum_name": ""}
    #     else:
    #         q_object = cam_query.pop(0)
    #         row[1] = {"forum_id": q_object.forum_id, "forum_name": q_object.forum_name}
    #     if dom_query == []:
    #         row[2] = {"forum_id": "", "forum_name": ""}
    #     else:
    #         q_object = dom_query.pop(0)
    #         row[2] = {"forum_id": q_object.forum_id, "forum_name": q_object.forum_name}
    #     if escort_query == []:
    #         row[3] = {"forum_id": "", "forum_name": ""}
    #     else:
    #         q_object = escort_query.pop(0)
    #         row[3] = {"forum_id": q_object.forum_id, "forum_name": q_object.forum_name}
    #     if porn_query == []:
    #         row[4] = {"forum_id": "", "forum_name": ""}
    #     else:
    #         q_object = porn_query.pop(0)
    #         row[4] = {"forum_id": q_object.forum_id, "forum_name": q_object.forum_name}
    #     if dance_query == []:
    #         row[5] = {"forum_id": "", "forum_name": ""}
    #     else:
    #         q_object = dance_query.pop(0)
    #         row[5] = {"forum_id": q_object.forum_id, "forum_name": q_object.forum_name}
    #     if phone_query == []:
    #         row[6] = {"forum_id": "", "forum_name": ""}
    #     else:
    #         q_object = phone_query.pop(0)
    #         row[6] = {"forum_id": q_object.forum_id, "forum_name": q_object.forum_name}
    #     if sugar_query == []:
    #         row[7] = {"forum_id": "", "forum_name": ""}
    #     else:
    #         q_object = sugar_query.pop(0)
    #         row[7] = {"forum_id": q_object.forum_id, "forum_name": q_object.forum_name}
    #     if other_query == []:
    #         row[8] = {"forum_id": "", "forum_name": ""}
    #     else:
    #         q_object = other_query.pop(0)
    #         row[8] = {"forum_id": q_object.forum_id, "forum_name": q_object.forum_name}
    #     all_forums.append(row)


    #Checks to see if the user is logged in. If so, renders forums
    if 'current_user' in list(session.keys()):
        return render_template("forums.html", cam=cam, dom=dom, escort=escort,
                               porn=porn, dance=dance, phone=phone, other=other, sugar=sugar,
                               cam_query=cam_query, dom_query=dom_query, escort_query=escort_query,
                               porn_query=porn_query, dance_query=dance_query, phone_query=phone_query,
                               sugar_query=sugar_query, other_query=other_query)

    #Otherwise it redirects to the login page
    else:
        flash("Please login before entering the forums.")
        return redirect("/login")


@app.route("/forums/parent/<forum_id>/<page_num>", methods=["POST"])
def add_post(forum_id, page_num=1):
    """Uses POST request to create a new post within a forum (Tested)"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    sugar = Forum.query.filter_by(forum_id=7).one()
    other = Forum.query.filter_by(forum_id=8).one()

    #Creates lists for all of the children forums of the main 8 forums
    cam_query = Forum.query.filter_by(parent_forum_id=1).all()
    dom_query = Forum.query.filter_by(parent_forum_id=2).all()
    escort_query = Forum.query.filter_by(parent_forum_id=3).all()
    porn_query = Forum.query.filter_by(parent_forum_id=4).all()
    dance_query = Forum.query.filter_by(parent_forum_id=5).all()
    phone_query = Forum.query.filter_by(parent_forum_id=6).all()
    sugar_query = Forum.query.filter_by(parent_forum_id=7).all()
    other_query = Forum.query.filter_by(parent_forum_id=8).all()

    #Gets the new posts content
    post_content = request.form['content']

    #Checks to see the users info and which posts they have flagged
    user = User.query.filter_by(email=session['current_user']).one()
    flag_query = Flag.query.filter(Flag.user_id == User.user_id).all()
    flags = []
    if len(flag_query) > 0:
        for item in flag_query:

            flags.append(item.post_id)

    #Adds the new post to the database
    new_post = Post(parent_post_id=0, user_id=user.user_id, username=user.username,
                    forum_id=forum_id, content=post_content, p_datetime=datetime.now(),
                    date_posted=(str(datetime.now())[:16]))

    #Doublechecks that the user isn't creating a duplicate post
    if Post.query.filter(Post.content == new_post.content,
                         Post.username == new_post.username).all() == []:
        db.session.add(new_post)
        db.session.commit()

    #Redirects everything back to the same forum page
    return redirect("/forums/order_by_date/" + str(forum_id) + "/" + str(page_num))


@app.route("/forums/child/<post_id>", methods=["POST"])
def add_child_post(post_id, page_num=1):
    """Uses POST request to create a new child (response) post within a forum (Tested)"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    sugar = Forum.query.filter_by(forum_id=7).one()
    other = Forum.query.filter_by(forum_id=8).one()

    #Creates lists for all of the children forums of the main 8 forums
    cam_query = Forum.query.filter_by(parent_forum_id=1).all()
    dom_query = Forum.query.filter_by(parent_forum_id=2).all()
    escort_query = Forum.query.filter_by(parent_forum_id=3).all()
    porn_query = Forum.query.filter_by(parent_forum_id=4).all()
    dance_query = Forum.query.filter_by(parent_forum_id=5).all()
    phone_query = Forum.query.filter_by(parent_forum_id=6).all()
    sugar_query = Forum.query.filter_by(parent_forum_id=7).all()
    other_query = Forum.query.filter_by(parent_forum_id=8).all()

    #Gets the new posts content
    post_content = request.form['child_content']

    #Checks to see the users info and which posts they have flagged
    user = User.query.filter_by(email=session['current_user']).one()
    flag_query = Flag.query.filter(Flag.user_id == User.user_id).all()
    flags = []
    if len(flag_query) > 0:
        for item in flag_query:
            flags.append(item.post_id)

    #Queries the data for the parent post
    parent_post = Post.query.filter_by(post_id=post_id).one()

    #Adds the new post to the database
    new_post = Post(user_id=user.user_id, username=user.username, forum_id=parent_post.forum_id,
                    parent_post_id=post_id, content=post_content, p_datetime=datetime.now(),
                    date_posted=(str(datetime.now())[:16]))

    #Doublechecks that the user isn't creating a duplicate post
    if Post.query.filter(Post.content == post_content, Post.username == user.username).all() == []:
        db.session.add(new_post)
        db.session.commit()

    #Redirects everything back to the same forum page
    return  redirect("/forums/order_by_date/" + str(parent_post.forum_id) + "/" + str(page_num))


@app.route("/forums/edit/<post_id>", methods=["POST"])
def edit_post(post_id):
    """Uses POST request edit an already-existing dicsussion post (Tested)"""


    #Gets the post's new content
    post_content = request.form['child_content']

    #Updates post content
    (db.session.query(Post).filter_by(post_id=post_id).update(
        {'content': post_content, 'edit_datetime': datetime.now()}))
    db.session.commit()

    #Queries the parent post to double-check the forum_id
    parent_post = Post.query.filter_by(post_id=post_id).one()

    #Redirects everything back to the same forum page
    return redirect('/forums/order_by_date/' + str(parent_post.forum_id) + "/1")


@app.route("/forums/delete/<post_id>", methods=["POST"])
def delete_post(post_id):
    """Uses POST request to create a new post within a forum (Tested)"""

    #Gets the new posts content
    post_content = str(request.form['delete_check'])
    #Updates post content
    if post_content == "Yes":
        (db.session.query(Post).filter_by(post_id=post_id).update(
            {'content': 'This post has been deleted by its poster.',
             'edit_datetime': datetime.now(), 'deleted': True}))
        db.session.commit()

    #Queries the parent post to double-check the forum_id
    parent_post = Post.query.filter_by(post_id=post_id).one()

    #Redirects everything back to the same forum page
    return redirect('/forums/order_by_date/' + str(parent_post.forum_id) + "/1")



@app.route("/forums/like/<post_id>", methods=["GET"])
def add_like(post_id):
    """When the user "likes" a post, it adds it to the dbase and updates page with new
     like info (Tested)"""

    #Queries from all of the dbase tables that need to be updated and/or rendered
    user_id = User.query.filter_by(email=session['current_user']).one().user_id
    forum_id = Post.query.filter_by(post_id=post_id).one().forum_id
    like_query = Like.query.filter(Like.post_id == post_id, Like.user_id == user_id).all()
    post_query = db.session.query(Post).filter_by(post_id=post_id).one()

    #If the user hasn't already liked/disliked the post, it adds the like to the dbase
    if like_query == []:
        new_like = Like(user_id=user_id, post_id=post_id, like_dislike="like")
        db.session.query(Post).filter_by(post_id=
                                         post_id).update({"like_num": (post_query.like_num + 1)})
        db.session.add(new_like)
        db.session.commit()

    #If the user previously disliked the comment, it updates it to a like
    elif like_query[0].like_dislike == "dislike":
        db.session.query(Like).filter(Like.post_id == post_id,
                                      Like.user_id == user_id).update({"user_id": user_id,
                                                                       "post_id": post_id,
                                                                       "like_dislike": "like"})
        (db.session.query(Post).filter_by(post_id=post_id).update(
            {"like_num": (post_query.like_num + 1), "dislike_num": (post_query.dislike_num - 1)}))
        db.session.commit()

    #Re-renders the forum page with the updated like info
    return redirect("/forums/order_by_date/{}/1".format(forum_id))


@app.route("/forums/dislike/<post_id>", methods=["GET"])
def add_dislike(post_id):
    """When the user "dislikes" a post, it adds it to the dbase & updates page with new like info (Tested)"""

    #Queries from all of the dbase tables that need to be updated and/or rendered
    user_id = User.query.filter_by(email=session['current_user']).one().user_id
    forum_id = Post.query.filter_by(post_id=post_id).one().forum_id
    like_query = Like.query.filter(Like.post_id == post_id, Like.user_id == user_id).all()
    post_query = db.session.query(Post).filter_by(post_id=post_id).one()

    #If the user hasn't already liked/disliked the post, it adds the dislike to the dbase
    if like_query == []:
        new_dislike = Like(user_id=user_id, post_id=post_id, like_dislike="dislike")
        (db.session.query(Post).filter_by(post_id=post_id).update(
            {"dislike_num": (post_query.dislike_num + 1)}))
        db.session.add(new_dislike)
        db.session.commit()

    #If the user previously liked the comment, it updates it to a dislike
    else:
        (db.session.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).update(
            {"user_id": user_id, "post_id": post_id, "like_dislike": "dislike"}))
        (db.session.query(Post).filter_by(post_id=post_id).update(
            {"dislike_num": (post_query.dislike_num + 1), "like_num": (post_query.like_num - 1)}))
        db.session.commit()

    #Re-renders the forum page with the updated dislike info
    return redirect("/forums/order_by_date/{}/1".format(forum_id))


@app.route("/forums/flag/<post_id>", methods=["POST"])
def flag_post(post_id):
    """When a user submitts a flag for removal, adds it to the dbase and refreshes page  (Tested)"""

    #Queries from all of the dbase tables that need to be updated and/or rendered
    user_id = User.query.filter_by(email=session['current_user']).one().user_id
    forum_id = Post.query.filter_by(post_id=post_id).one().forum_id
    flag_query = Flag.query.filter(Flag.post_id == post_id, Flag.user_id == user_id).all()
    post_query = db.session.query(Post).filter_by(post_id=post_id).one()

    #Gets the flag type from the flag form submission
    f_type = request.form['flag_rad']

    #Doublecheck the user hasn't already liked the post and then updates the dbase
    if flag_query == []:
        new_flag = Flag(user_id=user_id, post_id=post_id, flag_type=f_type)
        db.session.query(Post).filter_by(post_id=
                                         post_id).update({"flag_num": (post_query.flag_num + 1)})
        db.session.add(new_flag)
        db.session.commit()

    #Flashes message and re-renders the forum page
        flash('Your report has been submitted!')
    return redirect("/forums/order_by_date/{}/1".format(forum_id))


@app.route("/forums/order_by_date/<forum_id>/<page_num>")
def date_order(forum_id, page_num=1):
    """Renders forum page with posts ordered by date  (Tested, but not the actual order)"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    sugar = Forum.query.filter_by(forum_id=7).one()
    other = Forum.query.filter_by(forum_id=8).one()

    #Creates lists for all of the children forums of the main 8 forums
    cam_query = Forum.query.filter_by(parent_forum_id=1).all()
    dom_query = Forum.query.filter_by(parent_forum_id=2).all()
    escort_query = Forum.query.filter_by(parent_forum_id=3).all()
    porn_query = Forum.query.filter_by(parent_forum_id=4).all()
    dance_query = Forum.query.filter_by(parent_forum_id=5).all()
    phone_query = Forum.query.filter_by(parent_forum_id=6).all()
    sugar_query = Forum.query.filter_by(parent_forum_id=7).all()
    other_query = Forum.query.filter_by(parent_forum_id=8).all()

    #Queries from all of the dbase tables that need to be updated and/or rendered
    posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id == 0, Post.deleted == False).order_by(asc(Post.post_id)).all()
    child_posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id != 0).order_by(asc(Post.post_id)).all()
    users = Post.query.all()
    user = User.query.filter_by(email=session['current_user']).one()
    flag_query = Flag.query.filter(Flag.user_id == User.user_id).all()
    forum = Forum.query.filter_by(forum_id=forum_id).one()
    post_index=int(math.ceil((len(posts)/float(10))))

    print(posts)
    if posts:
        print(posts[0].forum_id)

    #Defines empty flag list to be filled with user's flags
    flags = []
    if len(flag_query) > 0:
        for item in flag_query:
            flags.append(item.post_id)

    #Renders Page
    return render_template("forum_page.html", users=users, forum=forum, cam=cam, dom=dom, escort=escort,
                           porn=porn, dance=dance, phone=phone, posts=posts, user=user,
                           child_posts=child_posts, flags=flags, flagnum=0, other=other, sugar=sugar, post_index=post_index, current_page=int(page_num),
                               cam_query=cam_query, dom_query=dom_query, escort_query=escort_query,
                               porn_query=porn_query, dance_query=dance_query, phone_query=phone_query,
                               sugar_query=sugar_query, other_query=other_query)


@app.route("/forums/order_by_pop/<forum_id>/<page_num>")
def pop_order(forum_id, page_num=1):
    """Renders forum page with posts ordered by popularity (Tested, but not the actual order)"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    sugar = Forum.query.filter_by(forum_id=7).one()
    other = Forum.query.filter_by(forum_id=8).one()

    #Creates lists for all of the children forums of the main 8 forums
    cam_query = Forum.query.filter_by(parent_forum_id=1).all()
    dom_query = Forum.query.filter_by(parent_forum_id=2).all()
    escort_query = Forum.query.filter_by(parent_forum_id=3).all()
    porn_query = Forum.query.filter_by(parent_forum_id=4).all()
    dance_query = Forum.query.filter_by(parent_forum_id=5).all()
    phone_query = Forum.query.filter_by(parent_forum_id=6).all()
    sugar_query = Forum.query.filter_by(parent_forum_id=7).all()
    other_query = Forum.query.filter_by(parent_forum_id=8).all()

    #Queries from all of the dbase tables that need to be updated and/or rendered
    posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id == 0, Post.deleted == False).order_by(desc(Post.like_num)).all()
    child_posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id != 0).order_by(desc(Post.like_num)).all()
    user = User.query.filter_by(email=session['current_user']).one()
    flag_query = Flag.query.filter(Flag.user_id == User.user_id).all()
    forum = Forum.query.filter_by(forum_id=forum_id).one()
    post_index=int(math.ceil((len(posts)/float(10))))
    #Defines empty flag list to be filled with user's flags
    flags = []
    if len(flag_query) > 0:
        for item in flag_query:
            flags.append(item.post_id)

    #Renders Page
    return render_template("forum_page.html", forum=forum, cam=cam, dom=dom, escort=escort, user=user,
                           porn=porn, dance=dance, phone=phone, posts=posts,
                           child_posts=child_posts, flags=flags, flagnum=0, other=other, sugar=sugar,
                           post_index=post_index, current_page=1,
                           cam_query=cam_query, dom_query=dom_query, escort_query=escort_query,
                           porn_query=porn_query, dance_query=dance_query, phone_query=phone_query,
                           sugar_query=sugar_query, other_query=other_query)


@app.route("/report", methods=["GET"])
def report_page():
    """If user logged in, renders report form page, otherwise redirects to login"""

    if 'current_user' in list(session.keys()):
        return render_template("report_form.html")
    else:
        flash('You must sign in before making a report.')
        return redirect("/login")



@app.route("/report", methods=["POST"])
def submit_form():
    """Submits the report form and saves incident to database"""

    #Queries dBase and gets info from form to be saves as new incident
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
    year = date[0:4]

    #Creates new incident and commits it to dBase
    new_report = Incident(year=year, user_id=user_id, police_dept_id=3, source_id=3,
                          inc_type=inc_type, address=address, city=city, state=state, latitude=lat,
                          longitude=lng, date=date, time=time, description=description,
                          sting_strat=sting, avoidance=avoid, other=other)
    new_cop = Cop(user_id=user_id, police_dept_id=3, cop_name=p_name, cop_badge=badge, cop_desc=p_description)
    db.session.add(new_report)
    db.session.add(new_cop)
    db.session.commit()

    #Redirects to homepage
    flash('Your report has been filed and should be added to the map soon!')
    return redirect("/")



@app.route("/profile")
def user_profile():
    """Renders user's profile"""

    user = User.query.filter_by(email=session['current_user']).one()

    return render_template("user_page.html", user=user, email=user.email, username=user.username,
                           fname=user.fname, lname=user.lname, about_me=user.description, tagline=user.tagline, location=user.location)



@app.route("/edit_profile", methods=["GET"])
def edit_page():
    """Renders the edit profile page"""

    user = User.query.filter_by(email=session['current_user']).one()

    return render_template("edit_profile.html", email=user.email, username=user.username,
                           fname=user.fname, lname=user.lname, about_me=user.description, user=user)



@app.route("/edit_profile", methods=["POST"])
def edit_profile():
    """Submits the profile edits"""


    #Gets info from html form and dbase
    email_input = request.form['email_input']
    pw_input = request.form['password']
    username = request.form['username']
    fname = request.form['fname']
    tagline = request.form['tagline']
    location = request.form['location']
    lname = request.form['lname']
    about_me = request.form['about_me']
    email2 = request.form['email_input2']
    phone = request.form['phone']
    timezone = request.form['timezone']
    user = User.query.filter_by(email=session['current_user']).one()


    p_word = user.password
    if isinstance(pw_input, str):
        pw_input = bytes(pw_input, 'utf-8')
    passwd = bytes(p_word, 'utf-8')

    if bcrypt.hashpw(pw_input, passwd) == passwd:
        (db.session.query(User).filter(
            User.email == session['current_user']).update(
                {'fname': fname, 'lname': lname, 'email': email_input,
                 'username': username, 'description': about_me, 'email2': email2, 'phone': phone,
                 'timezone': timezone}))
        db.session.commit()
        flash('Your Profile was Updated!')
        return redirect("/profile")
        

    #Otherwise, it flashes a message and redirects to the login page
    else:
        flash('Your e-mail or password was incorrect! Please try again or Register.')
        return redirect("/edit_profile")

@app.route("/contact")
def contact_us():
    """Renders the 'contact us' page"""
    return render_template("contact.html")

@app.route("/resources")
def resources():
    """Renders the 'additional resources' page"""
    return render_template("resources.html")

@app.route("/sw_main")
def safewalk_main():
    """Renders the main safewalk page including a user's alert-sets"""

    #Creates variables for the curent time, date, and datetime for convenience
    time = datetime.datetime.now().time()
    date = (datetime.datetime.today())
    now = datetime.datetime.now()

    #Queries the dBase for the current user and their alerts and contacts
    if 'current_user' in session:
        user = User.query.filter_by(email=session['current_user']).one()
    else:
        return redirect('/login')

    alert_sets = AlertSet.query.filter_by(user_id=user.user_id).all()
    al_sets = []
    alerts = Alert.query.filter_by(user_id=user.user_id).all()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()
    con_length = len(contacts)

    #If the user has added no contacts, they are re-routed to the 'getting started' page
    if con_length < 1:
        return redirect("/sw_getting_started")

    #Loops through all user's alert-sets and initiates variables to keep track of them
    for a_set in alert_sets:
        print(a_set)
        aset_alerts = []
        a_set.total = 0

        #Loops through the alerts and adds the datetime for each to the aset_alerts list
        for alert in alerts:
            print(alert)
            if alert.active == True:
                print(alert)
            if a_set.alert_set_id == alert.alert_set_id and a_set.interval and alert.active == False:
                tim = now + datetime.timedelta(minutes=a_set.interval)
                aset_alerts.append(tim)
                print(tim)
            elif a_set.alert_set_id == alert.alert_set_id and a_set.interval and alert.active == True:
                aset_alerts.append(alert.datetime)
                print(alert.datetime)
            elif a_set.alert_set_id == alert.alert_set_id and alert.active == True:
                dtime = alert.datetime
                aset_alerts.append(dtime)
            elif a_set.alert_set_id == alert.alert_set_id and alert.active == False:
                dtime = datetime.datetime.combine(date, alert.time)
                aset_alerts.append(dtime)

        """If there is at least one alert for each alert-set, the earliest alert and
        the total number of seconds until that alert are saved to the alert-set object"""
        if len(aset_alerts) >= 1:
            if aset_alerts[0] != []:
                print('aset_alerts:')
                print(aset_alerts)
                aset_alerts.sort()
                print('aset_alerts0:')
                print(aset_alerts[0])
                print(now)
                a_set.next_alarm = aset_alerts[0]
                a_set.next_alarm_dis = aset_alerts[0].strftime("%I:%M %p, %m/%d/%Y")
                d1 = now - aset_alerts[0]
                print(d1)
                d2 = abs(d1.total_seconds())
                # days = math.floor(d2 / 86400)
                # hours = math.floor((d2 - (days * 86400)) / 3600)
                # minutes = math.floor((d2 - (days * 86400) - (hours * 3600)) / 60)
                # seconds = math.floor(d2 - (days * 86400) - (hours * 3600) - (minutes * 60))
                # print(minutes)
                # a_set.countdown = datetime.time(int(hours), int(minutes), int(seconds))
                # a_set.days = int(days)
                # a_set.hours = int(hours)
                # a_set.minutes = int(minutes)
                # a_set.seconds = int(seconds)
                a_set.total =int(d2)
                # if d1 < datetime.timedelta(seconds=0):
                #     a_set.total = 0
                print(a_set.total)
            else:
                a_set.next_alarm_dis = now.strftime("%I:%M %p, %m/%d/%Y")

        #If there are no alerts, the current datetime is used as a placeholder
        else:a_set.next_alarm_dis = now.strftime("%I:%M %p, %m/%d/%Y")

    for a_s in alert_sets:
        if len(a_s.a_name) > 14:
            a_s.a_name = a_s.a_name[:9] + "..." + a_s.a_name[-4:]


    return render_template("safewalk_main.html", alert_sets=alert_sets, timezone=user.timezone, user=user)

@app.route("/sw_getting_started")
def get_started():
    """Renders the 'Getting Started with SafeWalk' Page"""

    #Queries the current user and their contact info
    user = User.query.filter_by(email=session['current_user']).one()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()
    con_length = len(contacts)

    return render_template("getting_started_safewalk.html", contacts=contacts, con_length=con_length, timezone=user.timezone)

@app.route("/rec_alerts")
def recurring_alerts():
    """Renders the 'Create a Recurring Alert-Set' Page"""

    #Queries the current user and their contact info
    user = User.query.filter_by(email=session['current_user']).one()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()

    return render_template("recurring_alerts.html", contacts=contacts, timezone=user.timezone)

@app.route("/sched_alerts")
def scheduled_alerts():
    """Renders the 'Create a Scheduled Alert-Set' Page"""

    #Queries the current user and their contact info
    user = User.query.filter_by(email=session['current_user']).one()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()

    return render_template("scheduled_alerts.html", contacts=contacts, timezone=user.timezone)


@app.route("/contacts")
def user_contacts():
    """Renders the User's 'contacts' Page"""

    #Queries the current user and their contact info
    user = User.query.filter_by(email=session['current_user']).one()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()

    return render_template("contacts.html", contacts=contacts, timezone=user.timezone)


@app.route("/contacts", methods=["POST"])
def add_contact():
    """Adds a user's new contact's info to the dBase"""

    #Creates variables from the form on the contacts page
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    c_type = request.form['c_type']
    message = request.form['message']

    #Queries the current user
    user = User.query.filter_by(email=session['current_user']).one()

    #Creates the new Contact object, adds it to the dBase and commits the addition
    new_contact = Contact(user_id=user.user_id, name=name, email=email, phone=phone, c_type=c_type, c_message=message)
    db.session.add(new_contact)
    db.session.commit()

    return redirect("/contacts")


@app.route("/del_contact/<contact_num>")
def delete_contact(contact_num):
    """Deletes a user's contact from the dBase"""

    #Queries the contact in question, deletes it from the dBase, and commits
    contact = Contact.query.filter_by(contact_id=contact_num).one()
    db.session.delete(contact)
    db.session.commit()

    return redirect("/contacts")


@app.route("/edit_contact/<contact_num>", methods=["POST"])
def edit_contact(contact_num):
    """Edit's a contact's info"""

    #Creates variables from the form on the contacts page
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    c_type = request.form['c_type']
    message = request.form['message']

    #Queries the contact in question, edits it in the dBase, and commits
    contact = Contact.query.filter_by(contact_id=contact_num).one()
    ((db.session.query(Contact).filter_by(contact_id=contact_num)).update(
    {'name':name, 'email':email, 'phone':phone, 'c_type':c_type, 'c_message':message}))
    db.session.commit()

    return redirect("/contacts")


@app.route("/add_recset", methods=["POST"])
def add_rec_alertset():
    """Adds a recurring Alert-Set to the dBase"""

    #Gets the alert and alert set info from the form on the add a new rec set page
    name = request.form['set_name']
    desc = request.form['descri']
    interval = request.form['interval']
    contacts = request.form.getlist('contact')

    #Queries the current user
    user = User.query.filter_by(email=session['current_user']).one()

    #Creates a new alert set, adds it to the dBase, commits, and then queries the just-created alert set
    new_alert_set = AlertSet(user_id=user.user_id, a_name=name, a_desc=desc, interval=interval)
    db.session.add(new_alert_set)
    db.session.commit()
    alert_set = AlertSet.query.filter(AlertSet.user_id == user.user_id, AlertSet.a_name == name).first()

    #Initiates 3 contact variables, sets the first to the first contact and the next two to None
    contact1 = int(contacts[0])
    contact2 = None
    contact3 = None

    #If more than one contact is associated with the alert set, the following variables are set to them
    if len(contacts) > 1:
        contact2 = int(contacts[1])
    if len(contacts) > 2:
        contact3 = int(contacts[2])

    #A new alert (associated with the alert set) is created, added, and commited to the dBase
    new_alert = Alert(alert_set_id=alert_set.alert_set_id, user_id=user.user_id, contact_id1=contact1,
                      contact_id2=contact2, contact_id3=contact3, interval=interval, message=desc)
    db.session.add(new_alert)
    db.session.commit()

    return redirect("/sw_main")

@app.route("/edit_recset/<alert_set_id>")
def edit_recset_page(alert_set_id):
    """Renders the page to edit a recurring alert set"""

    #Queries the user, alert_set, user's contacts, and associated alerts
    user = User.query.filter_by(email=session['current_user']).one()
    alert_set = AlertSet.query.filter_by(alert_set_id=alert_set_id).one()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()
    alert = Alert.query.filter_by(alert_set_id=alert_set_id).one()

    return render_template("edit_recurring_alerts.html", alert_set=alert_set, contacts=contacts, alert=alert, timezone=user.timezone)

@app.route("/save_recset/<alert_set_id>", methods=["POST"])
def save_recset(alert_set_id):
    """Saves the edits to a recurring alert set"""

    #Gets the alert and alert set info from the form
    name = request.form['set_name']
    desc = request.form['descri']
    interval = request.form['interval']
    contacts = request.form.getlist('contact')

    #The Alert-Set is updated in the dBase with the new data
    (db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id)).update(
    {'a_name': name, 'a_desc': desc, 'interval': interval})

    #Initiates 3 contact variables, sets the first to the first contact and the next two to None
    contact1 = int(contacts[0])
    contact2 = None
    contact3 = None

    #If more than one contact is associated with the alert set, the following variables are set to them
    if len(contacts) > 1:
        contact2 = int(contacts[1])
    if len(contacts) > 2:
        contact3 = int(contacts[2])

    #The alert associated with the alert set is then updated and all of the changes are committed
    (db.session.query(Alert).filter_by(alert_set_id=alert_set_id)).update(
    {'message': desc, 'interval': interval, 'contact_id1': contact1, 'contact_id2': contact2, 'contact_id3': contact3})
    db.session.commit()

    #The user is then re-routed to the main safewalk page
    return redirect("/sw_main")

@app.route("/add_schedset", methods=["POST"])
def add_sched_alertset():
    """Adds a new scheduled alert set"""

    #Iniates date and end date variables and sets them to None
    date = None
    end_date = None

    #If the user enters a date or end_date, the variables are then updated to that value
    if len(request.form['date']) > 2:
        date = request.form['date']
    if len(request.form['end_date']) > 2:
        end_date = request.form['end_date']

    #Gets the alert set name, description, and then queries the current user
    name = request.form['set_name']
    desc = request.form['descri']
    user = User.query.filter_by(email=session['current_user']).one()

    #A new alert set object is then created, added to the dBase, and commited
    new_alert_set = AlertSet(user_id=user.user_id, a_name=name, a_desc=desc, date=date, end_date=end_date)
    db.session.add(new_alert_set)
    db.session.commit()

    #The just-created alert set is then queried to get the alert_set_id
    alert_set = AlertSet.query.filter(AlertSet.user_id == user.user_id, AlertSet.a_name == name).first()

    #The user is then redirected to the scheduled set edit page for this alert set
    return redirect("/edit_schedset/" + str(alert_set.alert_set_id))

@app.route("/edit_schedset/<alert_set_id>")
def edit_schedset_page(alert_set_id):
    """Renders the page where a scheduled alert set can be edited"""

    #The user, their alert_sets, alerts, and contacts are queried
    user = User.query.filter_by(email=session['current_user']).one()
    alert_set = AlertSet.query.filter_by(alert_set_id=alert_set_id).one()
    alerts = Alert.query.filter_by(alert_set_id=alert_set_id).order_by(asc(Alert.alert_id)).all()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()

    #This information is then sent to the rendered edit page
    return render_template("edit_sched_alerts.html", alert_set=alert_set, contacts=contacts, alerts=alerts, timezone=user.timezone)

@app.route("/edit_set/<alert_set_id>", methods=["POST"])
def save_schedset(alert_set_id):
    """Saves the scheduled alert set beind edited"""

    #Gets the alert set details from the form
    date = request.form['date']
    end_date = request.form['end_date']
    name = request.form['set_name']
    desc = request.form['descri']

    #Queries the dBase for the alert set, updates it, commits, and redirects the user back to edit page
    (db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id)).update(
    {'date': date, 'end_date': end_date, 'a_name': name, 'a_desc': desc})
    db.session.commit()
    return redirect("/edit_schedset/" + str(alert_set_id))

@app.route("/edit_al/<alert_id>", methods=["POST"])
def edit_schedal(alert_id):
    """Saves the existing scheduled alert being edited"""

    #Queries alert in question current user
    alert = Alert.query.filter_by(alert_id=alert_id).one()
    user = User.query.filter_by(email=session['current_user']).one()

    #Gets the alert information from the form on the page
    time = request.form['time']
    contacts = request.form.getlist('contact')
    message = request.form['check_mess']

    #Initiates 3 contact variables, sets the first to the first contact and the next two to None
    contact1 = int(contacts[0])
    contact2 = None
    contact3 = None

    #If more than one contact is associated with the alert set, the following variables are set to them
    if len(contacts) > 1:
        contact2 = int(contacts[1])
    if len(contacts) > 2:
        contact3 = int(contacts[2])

    #Queries and updates the alert, commits, and redirects back to the edit page
    (db.session.query(Alert).filter_by(alert_id=alert_id)).update(
    {'time': time, 'contact_id1': contact1, 'contact_id2': contact2, 'contact_id3': contact3, 'message': message})
    db.session.commit()
    return redirect("/edit_schedset/" + str(alert.alert_set_id))

@app.route("/add_alert/<alert_set_id>", methods=["POST"])
def add_sched_alert(alert_set_id):
    """Saves a new scheduled alert"""

    #Queries the current user
    user = User.query.filter_by(email=session['current_user']).one()
    
    #Gets the alert info from the form on the edit sched set page
    time = request.form['time']
    contacts = request.form.getlist('contact')
    message = request.form['check_mess']
    
    #Initiates 3 contact variables, sets the first to the first contact and the next two to None
    contact1 = int(contacts[0])
    contact2 = None
    contact3 = None
    
    #If more than one contact is associated with the alert set, the following variables are set to them
    if len(contacts) > 1:
        contact2 = int(contacts[1])
    if len(contacts) > 2:
        contact3 = int(contacts[2])
    
    #Creates a new alert object, adds it to the dBase, commits, and redirects back to the edit page
    new_alert = Alert(alert_set_id=alert_set_id, user_id=user.user_id, contact_id1=contact1,
                      contact_id2=contact2, contact_id3=contact3, message=message, time=time)
    db.session.add(new_alert)
    db.session.commit()
    return redirect("/edit_schedset/" + str(alert_set_id))

@app.route("/activate/<alert_set_id>")
def activate_alertset(alert_set_id):
    """Activates an alert set"""

    #The alert set in question is queried
    alert_set = AlertSet.query.filter_by(alert_set_id=alert_set_id).one()
    
    #Variables set to the current date, time, and datetime are created for convenience
    time = datetime.datetime.now().time()
    date = (datetime.datetime.today())
    dt = datetime.datetime.now()
    
    #An empty list is created to store the datetimes of the alerts associated with the alert set
    dt_list = []
    
    #If there is no start date, the start date is set to today
    if alert_set.date == None:
        db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id).update({'date': date, 'start_datetime': dt})
    
    #If the alert set is scheduled (not recurring), the alert times are added to the the dt_list
    if alert_set.interval == None:
        alerts = Alert.query.filter_by(alert_set_id=alert_set_id).all()
        for alert in alerts:
            db.session.query(Alert).filter_by(alert_id=alert.alert_id).update({'active': True, 'start_time': time})
            if alert.date == None:
                dtime = datetime.datetime.combine(date, alert.time)
                db.session.query(Alert).filter_by(alert_id=alert.alert_id).update({'date': date, 'datetime': dtime})
                dt_list.append(dtime)
            else:
                dtime = datetime.datetime.combine(alert.date, alert.time)
                db.session.query(Alert).filter_by(alert_id=alert.alert_id).update({'datetime': dtime})
                dt_list.append(dtime)
    
    #If the alert set is recurring, the alert time is set to now + the time interval
    else:
        print("Interval = " + str(alert_set.interval))
        print("Rec Activated")
        # dtime = datetime.datetime.combine(date, time)
        # dt_list.append(dtime)
        dtime_int = dt + datetime.timedelta(minutes=alert_set.interval)
        alert = Alert.query.filter_by(alert_set_id=alert_set_id).one()
        db.session.query(Alert).filter_by(alert_id=alert.alert_id).update({'active': True, 'start_time': time, 'time': dtime_int.time(), 'datetime': dtime_int})
        dt_list.append(dtime_int)
    
    #The alert set is updated to be active and its commited
    db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id).update({'active': True, 'start_time': time, 'start_datetime': dt})
    db.session.commit()
    
    #The alert datetime list is sorted and the earliest time is then sent back to the page
    dt_list.sort()
    alarm_dt = dt_list[0].strftime("%I:%M %p, %m/%d/%Y")
    return str(alarm_dt)

@app.route("/deactivate/<alert_set_id>")
def deactivate_alertset(alert_set_id):
    """Deactivates an alert set"""

    #The alert set is queried and updated
    (db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id)).update(
    {'active': False})
    
    #All alerts associated with the alert set are queried and updated, and it's all commited
    alerts = Alert.query.filter_by(alert_set_id=alert_set_id).all()
    for alert in alerts:
        if alert.interval:
            db.session.query(Alert).filter_by(alert_id=alert.alert_id).update(
            {'active': False, 'checked_in': False, 'time': None, 'datetime': None})
        else:
            db.session.query(Alert).filter_by(alert_id=alert.alert_id).update(
            {'active': False, 'checked_in': False,'datetime': None})
    db.session.commit()
    return "Alert Set Deactivated"

@app.route("/check_ins")
def checkin_page():
    """Renders the User's check-in page"""

    #The current user and check-ins are queried and the page is rendered
    user = User.query.filter_by(email=session['current_user']).one()
    check_ins = CheckIn.query.filter_by(user_id=user.user_id).all()
    return render_template("checkins_page.html", check_ins=check_ins, timezone=user.timezone)

@app.route("/add_check_in", methods=["POST"])
def add_new_checkin():
    """Using POST, a new check-in is added from the check-in page"""

    #Get's the check-in details from the form on the page and runs the check_in helper-function
    text = request.form['check_text']
    user = User.query.filter_by(email=session['current_user']).one()
    
    #Use's the helper function check_in()
    check_in(user.user_id, text)
    
    #Queries the active and all alerts
    alerts = Alert.query.filter(Alert.user_id == user.user_id, Alert.active == True).all()
    all_alerts = Alert.query.filter(Alert.user_id == user.user_id).all()
    
    #Creates and empty list which is then filled with datetimes from the active alerts
    alert_datetimes = []
    for alert in alerts:
        if alert.datetime:
            alert_datetimes.append(alert.datetime)
    
    #The List of Datetimes is sorted
    alert_datetimes.sort()
    
    #If there is at least one active alert, a message is created with that info
    if len(alert_datetimes) > 0:
        diff = datetime.datetime.now() - alert_datetimes[0]
        minutes = (diff.total_seconds()) / 60
        time = alert_datetimes[0].time()
        check_time = (alert_datetimes[0] - datetime.timedelta(hours=1)).time()
        message = "Your Check-In has been received! Your next alarm is due in " + str(minutes) + " minutes, so you must check in between " + str(check_time) + " and " + str(time) + "."
    
    #Otherwise a message is created explaining that there are no active alerts
    else:
        message = "Your check-in has been received! You don't have any alerts currently active."
    
    #The message is then sent back to the user as confirmation
    if len(all_alerts) > 0:
        send_alert_user(all_alerts[0].alert_id, message)

    return redirect("/check_ins")

@app.route("/feedback", methods=["POST"])
def submit_feedback():
    """Using POST, feedback is added from the check-in page"""

    #Get's the Feedback details from the form on the page and adds it to the dBase
    text = request.form['feedback_text']
    user = User.query.filter_by(email=session['current_user']).one()
    dt = datetime.datetime.now()
    new_feedback = Feedback(user_id=user.user_id, datetime=dt, content=text)
    db.session.add(new_feedback)
    db.session.commit()
    return "Feedback Submitted!"

@app.route("/user_code", methods=["POST"])
def new_user_code():
    """Creates a new User Code"""
    
    user = User.query.filter_by(email=session['current_user']).one()
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    # code = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    code_check = User.query.filter_by(user_code=code).all()
    while len(code_check) > 0 or "0" in code or "O" in code:
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        # code = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
        code_check = User.query.filter_by(user_code=code).all()

    db.session.query(User).filter_by(user_id=user.user_id).update({'user_code': code})

    db.session.commit()

    return str(code)

@app.route("/incoming_mail", methods=["POST"])
def mailin():
    """Route where incoming mail is sent from mailgun"""

    #Access some of the email parsed values:
    sender = request.form['From']
    send_address = request.form['sender']
    subject = request.form['subject']
    text = request.form['body-plain']
    body = str(text)

    #The user is queried using the e-mail address
    user = User.query.filter_by(email=str.strip(send_address)).all()
    if user == []:
        user = User.query.filter_by(email2=str.strip(send_address)).all()

    if user != []:
        print("User Found by email address")

    while user == []:
        left = body.find("(")
        if left == -1:
            break
        else:
            right = body.find(")")
            if right == left + 5:
                user = User.query.filter_by(user_code=body[(left + 1):(left + 5)]).all()
                body = body[0:left] + body[(left + 1):]
                body = body[0:right] + body[(right + 1):]
                if user != []:
                    print("User Found by user code")
    
    if user == []:
        print("No User Was Found")
    else:
        send_email(send_address, "Thank You! Your Check-In has been received and logged!")

    #Assuming a user is found, the check-in helper-function is run
    if len(user) >= 1:
        u_id = user[0].user_id
        check_in(u_id, text)
    print(send_address)
    print("Email Message Received")
    return "Email Message Received"

@app.route('/incoming_sms', methods=['POST'])
def smsin():
    """Route where incoming SMS messages are sent from Bandwidth"""
    
    number = request.form['From']
    message_body = request.form['Body']
    body = str(message_body)

    # # Access some of the SMS parsed values:
    # dat = request.data
    # data = json.loads(dat.decode(encoding="utf-8", errors="strict"))
    # message_body = data['text']
    # phone = data['from']

    if len(number) > 10:
        number = number[-10:]

    print("Number =" + str(number))
    print("Body =" + body)


    #The user is queried using the phone-number

    user = User.query.filter_by(phone=str(number)).all()

    if user != []:
        print("User Found by phone number")

    while user == []:
        left = body.find("(")
        if left == -1:
            break
        else:
            right = body.find(")")
            if right == left + 5:
                user = User.query.filter_by(user_code=body[(left + 1):(left + 5)]).all()
                body = body[0:left] + body[(left + 1):]
                body = body[0:right] + body[(right + 1):]
                if user != []:
                    print("User Found by user code")
    
    if user == []:
        print("No User Was Found")
    else:
        send_message(number, "Thank You " + user[0].fname + "! Your Check-In has been received and logged!")
    
    #Assuming a user is found, the check-in helper-function is run
    if len(user) >= 1:
        u_id = user[0].user_id
        check_in(u_id, message_body)
    print(number)
    print(user)
    print("SMS Received")
    return "SMS Received"


@app.route('/pass_change', methods=['POST'])
def pass_change():
    old_pw = request.form['pw_old']
    new_pw1 = request.form['pw_new']
    new_pw2 = request.form['pw_new2']

    user_query = User.query.filter(User.email == email_input).all()
    pword = bytes(new_pw1, 'utf-8')
    hashed_word = bcrypt.hashpw(pword, bcrypt.gensalt()).decode('utf-8')
        #Queries to see if the email and pword match the database. If so, redirects to the safewalk page.

    p_word = user_query[0].password
    if isinstance(pw_input, str):
        pw_input = bytes(old_pw, 'utf-8')
    passwd = bytes(p_word, 'utf-8')


    if bcrypt.hashpw(pw_input, passwd) != passwd:
        flash('Your existing password is incorrect. Please Try again.')
        return redirect("/pass_page")

    #Otherwise, it re-renders the page and throws an error message to the user

    elif new_pw1 != new_pw2:
        flash("Your passwords don't match!")
        return redirect("/pass_page")

    else:
        (db.session.query(User).filter(
            User.email == session['current_user']).update(
                {'password': hashed_word}))
        db.session.commit()
        flash('Your Password was updated!')
        return redirect("/check_ins")

@app.route('/pass_reset', methods=['POST'])
def pass_reset():
    return redirect("/check_ins")

@app.route('/pass_code', methods=['POST'])
def pass_code():
    return redirect("/check_ins")



@app.route('/new_pass', methods=['POST'])
def new_pass():
    return redirect("/check_ins")

@app.route("/pass_page", methods=["GET"])
def pass_page():

    return render_template("pass_change.html")

@app.route("/pass_reset_page", methods=["GET"])
def pass_reset_page():

    return render_template("reset.html")

#####################################################

if __name__ == "__main__":
    start_runner()
    print("should be working")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    connect_to_db(app, 'postgresql:///safework')
    print("Connected to DB.")
    app.run()
