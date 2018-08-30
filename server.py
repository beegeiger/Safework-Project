"""SafeWork Server"""

from __future__ import absolute_import
from send_alerts import send_message, send_email
import flask
import bcrypt
import bcrypt
import math
import time
import json
import datetime
import threading
import secrets
from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (update, asc, desc)
from model import Forum, Post, User, Incident, Police, Source, Like, Flag, Contact, AlertSet, Alert, CheckIn, ReqCheck, connect_to_db, db, app
import requests
# from secrets_env import CLIENT_ID
import asyncio


db.init_app(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Causes error messages for undefined variables in jinja
app.jinja_env.undefined = StrictUndefined



####################################################################

def create_alert(alert_id):
    alert = Alert.query.filter_by(alert_id=alert_id).one()
    events = {}    
    user = User.query.filter_by(user_id=alert.user_id).one()
    alert_set = AlertSet.query.filter_by(alert_set_id=alert.alert_set_id).one()
    all_alerts = Alert.query.filter(alert.alert_set_id == alert.alert_set_id, alert.datetime > alert_set.start_datetime).all()
    check_ins = CheckIn.query.filter_by(user_id=user.user_id).all()
    message_body = """This is a Safety Alert sent by {} {} through the SafeWork Project SafeWalk Alert system, 
            found at safeworkproject.org \n \n""".format(user.fname, user.lname)
    if alert_set.notes:
        message_body += """The user has included the following messages when they made this alert and checked in \n \n {}""".format(alert_set.message)
    for a_a in all_alerts:
        if len(a_a.message) > 2:
            events[a_a.datetime] = a_a
    for chks in check_ins:
        events[chks.datetime] = chks
    for key in sorted(events.keys()):
        if events[key].alert_set_id and events[key].checked_in == True:
            message_body += "An alarm was scheduled for {} which {} checked-in for.".format(key, user.fname)
            if events[key].message:
                message_body += "The Alarm included the following notes: {} \n \n".format(events[key].message)
            else:
                message_body += "\n \n" 
        elif alert.datetime >= datetime.datetime.now() and events[key].message:
             message_body += "A future alarm is scheduled for {} and includes the notes: {}.".format(alert.datetime, events[key].message)
        elif events[key].alert_set_id:
            message_body += "An alarm was scheduled for {} which {} MISSED the checked-in for.".format(key, user.fname)
            if events[key].message:
                message_body += "The Alarm included the following notes: {} \n \n".format(events[key].message)
            else:
                message_body += "\n \n" 
        else:
            message_body += "{} checked in with the app at {} and included the following message: {}".format(user.fname, key, events[key].notes)
    if alert.contact_id3:
        message_body += """Two other contacts have been sent this alert. If you know who it might be,
                        consider reaching out and co-ordinating your effort to help {}.""".format(user.fname)
    elif alert.contact_id2:
        message_body += """One other contact has been sent this alert. If you know who it might be,
                        consider reaching out and co-ordinating your effort to help {}.""".format(user.fname)
    else:
        message_body += """You were the only person sent this alert, so if anything can be done
                        to help {}, it is up to you! Good luck!!!""".format(user.fname)
    return message_body

def send_alert(alert_id, message_body):
    alert = Alert.query.filter_by(alert_id=alert_id).one()
    user = User.query.filter_by(user_id=alert.user_id).one()
    if user.email2:
        send_email(user.email2, message_body)
    elif user.email:
        send_email(user.email, message_body)
    if user.phone:
        send_message(user.phone, message_body)
    return "Messages Sent"


def check_alerts():
    with app.app_context():
        print("Checking for Alerts Now: " + str(datetime.datetime.now()))
        alerts = Alert.query.filter_by(active=True).all()
        print(alerts)
        if len(alerts) > 0:
            for alert in alerts:
                difference = alert.datetime - datetime.datetime.now()
                if difference <= datetime.timedelta(minutes=1) and difference > datetime.timedelta(seconds=0):
                    checks = 0
                    check_ins = CheckIn.query.filter_by(user_id=alert.user_id).all()
                    for ch in check_ins:
                        dif = datetime.datetime.now() - alert.datetime
                        if dif <= timedelta(hours=1) and difference > timedelta(seconds=0):
                            checks += 1
                    if checks == 0:
                        print('A CHECK-IN WAS MISSED AND AN ALERT IS BEING SENT NOW!')
                        message_body = create_alert(alert.alert_id)
                        send_alert(alert.alert_id, message_body)
    return

#below is modified code from https://networklore.com/start-task-with-flask/
@app.before_first_request
def activate_job():
    def run_job():
        while True:
            check_alerts()
            time.sleep(60)

    thread = threading.Thread(target=run_job)
    thread.start()

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)
    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()



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
    pw_input = request.form['password'].encode('utf-8')
    username = request.form['username']
    tagline = request.form['tagline']
    location = request.form['location']
    hashed_word = bcrypt.hashpw(pw_input, bcrypt.gensalt())
    user_type = request.form['user_type']
    second_type = request.form['2nd']
    timezone = request.form['timezone']

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
        flash(email_input + " is not a valid e-mail address!")
        return render_template("register.html", email=email_input, username=username,
                               fname=fname, lname=lname, about_me=about_me)

    #Checking that the e-mail address hasn't already been registered
    elif User.query.filter_by(email=email_input).all() != []:
        flash(email_input + """This e-mail has already been registered! Either sign in with it,
                use a different e-mail address, or reset your password if you forgot it.""")
        return render_template("register.html", email=email_input, username=username, fname=fname,
                               lname=lname, about_me=about_me)

    #Checking that the username is available
    elif User.query.filter_by(username=username).all() != []:
        flash(email_input + "This username is already in use! Please try another one!")
        return render_template("register.html", email=email_input, username=username, fname=fname,
                               lname=lname, about_me=about_me)

    #Checking that the password length is at least 6
    elif len(pw_input) < 6:
        flash("Your password must be at least 5 characters long! Try again.")
        return render_template("register.html", email=email_input, username=username, fname=fname,
                               lname=lname, about_me=about_me)

    #Otherwise, the new user's information is added to the database
    else:
        new_user = User(email=email_input, password=hashed_word, username=username, fname=fname,
                        lname=lname, description=about_me, user_type_main=user_type,
                        user_type_secondary=second_type, tagline=tagline, location=location,
                        email2=email2, phone=phone, timezone=timezone)
        db.session.add(new_user)
        db.session.commit()
        #Code isn't working:
        # if user_type == "other":
        #     flash("""While you may enter the discussion forums if you are not a sex worker,
        #            keep in mind that this website is not intended for you. Do your best to respect
        #            the sex workers on this site as well as their experiences and thoughts. Also,
        #            please note that pimps and human traffickers are NOT welcome on this site. This
        #            site is intended for consensual sex workers working on their own
        #            volition ONLY.""")
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
    pw_input = request.form['pw_input'].encode('utf-8')
    user_query = User.query.filter(User.email == email_input).all()

    if user_query == []:
        flash('There is no record of your e-mail address! Please try again or Register.')
        return render_template("login.html")


    #Queries to see if the email and pword match the database. If so, redirects to forums.
    elif bcrypt.checkpw(pw_input, user_query[0].password.encode('utf-8')):
        session['current_user'] = email_input
        flash('You were successfully logged in')
        return redirect("/forums")

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

    #Redirects to homepage sudo apt-get install build-essential libffi-dev python-dev
    flash('Your report has been filed and should be added to the map soon!')
    return redirect("/")



@app.route("/profile")
def user_profile():
    """Renders user's profile"""

    user = User.query.filter_by(email=session['current_user']).one()

    return render_template("user_page.html", email=user.email, username=user.username,
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
    pw_input = request.form['old_password']
    new_password = request.form['new_password']
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

    #Checks that the password matches the user's password. If so, updates the user's info
    if User.query.filter(User.email == email_input, User.password == pw_input).all() != []:
        (db.session.query(User).filter(
            User.email == session['current_user'], User.password == pw_input).update(
                {'fname': fname, 'lname': lname, 'email': email_input, 'password': new_password,
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
    return render_template("contact.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/sw_main")
def safewalk_main():
    time = datetime.datetime.now().time()
    date = (datetime.datetime.today())
    now = datetime.datetime.now()
    user = User.query.filter_by(email=session['current_user']).one()
    alert_sets = AlertSet.query.filter_by(user_id=user.user_id).all()
    al_sets = []
    alerts = Alert.query.filter_by(user_id=user.user_id).all()
    for a_set in alert_sets:
        aset_alerts = []
        a_set.total = 0
        for alert in alerts:
            if a_set.alert_set_id == alert.alert_set_id and a_set.interval:
                aset_alerts.append(alert.datetime)
            elif a_set.alert_set_id == alert.alert_set_id:
                dtime = datetime.datetime.now()
                if time >= alert.time:
                    tomorrow = date + datetime.timedelta(days=1)
                    dtime = datetime.datetime.combine(tomorrow, alert.time)
                else:    
                    dtime = datetime.datetime.combine(date, alert.time)
                aset_alerts.append(dtime)
        if len(aset_alerts) >= 1:     
            aset_alerts.sort()
            print('aset_alerts:')
            print(aset_alerts[0])
            a_set.next_alarm = aset_alerts[0]
            a_set.next_alarm_dis = aset_alerts[0].strftime("%I:%M %p, %Y/%m/%d")
            d1 = abs(now - aset_alerts[0])
            d2 = float(d1.total_seconds())
            days = math.floor(d2 / 86400)
            hours = math.floor((d2 - (days * 86400)) / 3600)
            minutes = math.floor((d2 - (days * 86400) - (hours * 3600)) / 60)
            seconds = math.floor(d2 - (days * 86400) - (hours * 3600) - (minutes * 60))
            print(minutes)
            a_set.countdown = datetime.time(int(hours), int(minutes), int(seconds))
            a_set.days = int(days)
            a_set.hours = int(hours)
            a_set.minutes = int(minutes)
            a_set.seconds = int(seconds)
            a_set.total =int(d2)
            print(a_set.total)

    return render_template("safewalk_main.html", alert_sets=alert_sets, timezone=user.timezone)


@app.route("/rec_alerts")
def recurring_alerts():
    user = User.query.filter_by(email=session['current_user']).one()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()
    return render_template("recurring_alerts.html", contacts=contacts)

@app.route("/sched_alerts")
def scheduled_alerts():
    user = User.query.filter_by(email=session['current_user']).one()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()
    return render_template("scheduled_alerts.html", contacts=contacts)


@app.route("/contacts")
def user_contacts():
    user = User.query.filter_by(email=session['current_user']).one()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()
    return render_template("contacts.html", contacts=contacts)

@app.route("/contacts", methods=["POST"])
def add_contact():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    c_type = request.form['c_type']
    message = request.form['message']
    user = User.query.filter_by(email=session['current_user']).one()
    new_contact = Contact(user_id=user.user_id, name=name, email=email, phone=phone, c_type=c_type, c_message=message)
    db.session.add(new_contact)
    db.session.commit()
    return redirect("/contacts")

@app.route("/del_contact/<contact_num>")
def delete_contact(contact_num):
    contact = Contact.query.filter_by(contact_id=contact_num).one()
    db.session.delete(contact)
    db.session.commit()
    return redirect("/contacts")

@app.route("/edit_contact/<contact_num>", methods=["POST"])
def edit_contact(contact_num):
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    c_type = request.form['c_type']
    message = request.form['message']
    contact = Contact.query.filter_by(contact_id=contact_num).one()
    ((db.session.query(Contact).filter_by(contact_id=contact_num)).update(
    {'name':name, 'email':email, 'phone':phone, 'c_type':c_type, 'c_message':message}))
    db.session.commit()
    return redirect("/contacts")

@app.route("/add_recset", methods=["POST"])
def add_rec_alertset():
    name = request.form['set_name']
    desc = request.form['descri']
    interval = request.form['interval']
    contacts = request.form.getlist('contact')
    user = User.query.filter_by(email=session['current_user']).one()
    new_alert_set = AlertSet(user_id=user.user_id, a_name=name, a_desc=desc, interval=interval)
    db.session.add(new_alert_set)
    db.session.commit()
    alert_set = AlertSet.query.filter(AlertSet.user_id == user.user_id, AlertSet.a_name == name).first()
    contact1 = int(contacts[0])
    contact2 = None
    contact3 = None
    if len(contacts) > 1:
        contact2 = int(contacts[1])
    if len(contacts) > 2:
        contact3 = int(contacts[2])    
    new_alert = Alert(alert_set_id=alert_set.alert_set_id, user_id=user.user_id, contact_id1=contact1,
                      contact_id2=contact2, contact_id3=contact3, interval=interval, message=desc)
    db.session.add(new_alert)
    db.session.commit()
    alert_set = AlertSet.query.filter(AlertSet.user_id == user.user_id, AlertSet.a_name == name).first()
    return redirect("/sw_main")

@app.route("/edit_recset/<alert_set_id>")
def edit_recset_page(alert_set_id):
    user = User.query.filter_by(email=session['current_user']).one()
    alert_set = AlertSet.query.filter_by(alert_set_id=alert_set_id).one()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()
    alert = Alert.query.filter_by(alert_set_id=alert_set_id).one()
    return render_template("edit_recurring_alerts.html", alert_set=alert_set, contacts=contacts, alert=alert)

@app.route("/save_recset/<alert_set_id>", methods=["POST"])
def save_recset(alert_set_id):
    name = request.form['set_name']
    desc = request.form['descri']
    interval = request.form['interval']
    contacts = request.form.getlist('contact')
    (db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id)).update(
    {'a_name': name, 'a_desc': desc, 'interval': interval})
    contact1 = int(contacts[0])
    contact2 = None
    contact3 = None
    if len(contacts) > 1:
        contact2 = int(contacts[1])
    if len(contacts) > 2:
        contact3 = int(contacts[2])
    (db.session.query(Alert).filter_by(alert_set_id=alert_set_id)).update(
    {'message': desc, 'interval': interval, 'contact_id1': contact1, 'contact_id2': contact2, 'contact_id3': contact3})
    db.session.commit()
    return redirect("/sw_main")

@app.route("/add_schedset", methods=["POST"])
def add_sched_alertset():
    date = None
    end_date = None
    if len(request.form['date']) > 2:
        date = request.form['date']
    if len(request.form['end_date']) > 2:
        end_date = request.form['end_date']
    name = request.form['set_name']
    desc = request.form['descri']
    user = User.query.filter_by(email=session['current_user']).one()
    new_alert_set = AlertSet(user_id=user.user_id, a_name=name, a_desc=desc, date=date, end_date=end_date)
    db.session.add(new_alert_set)
    db.session.commit()
    alert_set = AlertSet.query.filter(AlertSet.user_id == user.user_id, AlertSet.a_name == name).first()
    return redirect("/edit_schedset/" + str(alert_set.alert_set_id))
    # return redirect("/sw_main")

@app.route("/edit_schedset/<alert_set_id>")
def edit_schedset_page(alert_set_id):
    user = User.query.filter_by(email=session['current_user']).one()
    alert_set = AlertSet.query.filter_by(alert_set_id=alert_set_id).one()
    alerts = Alert.query.filter_by(alert_set_id=alert_set_id).all()
    contacts = Contact.query.filter_by(user_id=user.user_id).order_by(asc(Contact.contact_id)).all()
    return render_template("edit_sched_alerts.html", alert_set=alert_set, contacts=contacts, alerts=alerts)

@app.route("/edit_set/<alert_set_id>", methods=["POST"])
def save_schedset(alert_set_id):
    date = request.form['date']
    end_date = request.form['end_date']
    name = request.form['set_name']
    desc = request.form['descri']
    (db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id)).update(
    {'date': date, 'end_date': end_date, 'a_name': name, 'a_desc': desc})    
    db.session.commit()
    return redirect("/edit_schedset/" + str(alert_set_id))

@app.route("/add_alert/<alert_set_id>", methods=["POST"])
def add_sched_alert(alert_set_id):
    user = User.query.filter_by(email=session['current_user']).one()
    time = request.form['time']
    contacts = request.form.getlist('contact')
    contact1 = int(contacts[0])
    contact2 = None
    contact3 = None
    if len(contacts) > 1:
        contact2 = int(contacts[1])
    if len(contacts) > 2:
        contact3 = int(contacts[2])
    message = request.form['check_mess']
    new_alert = Alert(alert_set_id=alert_set_id, user_id=user.user_id, contact_id1=contact1,
                      contact_id2=contact2, contact_id3=contact3, message=message, time=time)
    db.session.add(new_alert)
    db.session.commit()
    return redirect("/edit_schedset/" + str(alert_set_id))

@app.route("/activate/<alert_set_id>")
def activate_alertset(alert_set_id):
    print(alert_set_id)
    alert_set = AlertSet.query.filter_by(alert_set_id=alert_set_id).one()
    time = datetime.datetime.now().time()
    date = (datetime.datetime.today())
    dt = datetime.datetime.now()
    if alert_set.date == None:
        db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id).update({'date': date, 'start_datetime': dt})
    if alert_set.interval == None:
        print("step 1")
        alerts = Alert.query.filter_by(alert_set_id=alert_set_id).all()
        for alert in alerts:
            print("step 2")
            db.session.query(Alert).filter_by(alert_id=alert.alert_id).update({'active': True, 'start_time': time})
            if alert.date == None:
                print("step3a")
                print(time)
                print(alert.time)
                print(type(alert.time))
                dtime = datetime.datetime.combine(date, alert.time)
                print(dtime)
                db.session.query(Alert).filter_by(alert_id=alert.alert_id).update({'date': date, 'datetime': dtime})
            else:
                print("step 3b")
                dtime = datetime.datetime.combine(alert.date, alert.time)
                db.session.query(Alert).filter_by(alert_id=alert.alert_id).update({'datetime': dtime})
    else:
        print("Interval = " + str(alert_set.interval))
        print("Rec Activated")
        dtime = datetime.datetime.combine(date, time)
        dtime_int = dtime + datetime.timedelta(minutes=alert_set.interval)
        alert = Alert.query.filter_by(alert_set_id=alert_set_id).one()
        db.session.query(Alert).filter_by(alert_id=alert.alert_id).update({'active': True, 'start_time': time, 'start_time': time, 'datetime': dtime_int})
    db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id).update({'active': True, 'start_time': time, 'start_datetime': dt})
    db.session.commit()
    return "Alert Set Activated"

@app.route("/deactivate/<alert_set_id>")
def deactivate_alertset(alert_set_id):
    (db.session.query(AlertSet).filter_by(alert_set_id=alert_set_id)).update(
    {'active': False})
    alerts = Alert.query.filter_by(alert_set_id=alert_set_id).all()
    for alert in alerts:
        db.session.query(Alert).filter_by(alert_id=alert.alert_id).update(
        {'active': False})
    db.session.commit()
    return "Alert Set Deactivated"

@app.route("/incoming_mail", methods=["POST"])  
def mailin():  
    
    # access some of the email parsed values:
    sender = request.form['From']
    send_email = request.form['sender']
    subject = request.form['subject']
    text = request.form['body-plain']
    time = datetime.datetime.now().time()
    date = (datetime.datetime.today())
    datetime = datetime.datetime.now()
    user = User.query.filter_by(email=strp(send_email)).all()
    if len(user) >= 1:        
        new_check = CheckIn(user_id=user.user_id, notes=text, time=time, date=date, datetime=datetime)
        db.session.add(new_check)
        db.session.commit()
    print(send_email)
    print("Email Message Received")
    return "Email Message Received"

@app.route('/incoming_sms', methods=['POST'])
def smsin():
    number = request.form['From']
    message_body = request.form['Body']
    time = datetime.datetime.now().time()
    date = (datetime.datetime.today())
    datetime = datetime.datetime.now()
    user = User.query.filter_by(phone=str(number)).all()
    if len(user) >= 1:        
        new_check = CheckIn(user_id=user.user_id, notes=message_body, time=time, date=date, datetime=datetime)
        db.session.add(new_check)
        db.session.commit()
    print(number)
    print("SMS Received")
    return "SMS Received"


#####################################################

if __name__ == "__main__":
    start_runner()
    print("should be working")
    connect_to_db(app, 'postgresql:///safework')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print("Connected to DB.")
    app.run(host='0.0.0.0')
    

