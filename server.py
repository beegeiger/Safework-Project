"""SafeWork Server"""

from __future__ import absolute_import

import flask
import bcrypt
import bcrypt
import config
import json
import datetime
from datetime import datetime
from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (update, asc, desc)
from model import Forum, Post, User, Incident, Police, Source, Like, Flag, connect_to_db, db
import requests
from secrets_env import CLIENT_ID


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Causes error messages for undefined variables in jinja
app.jinja_env.undefined = StrictUndefined

####################################################################

@app.route("/")
def go_home():
    """Renders the safework homepage."""
    return render_template("homepage.html")


@app.route("/map")
def get_map():
    """Renders safework's arrest map."""
    return render_template("map_page.html")


@app.route("/incidents.json")
def get_points():
    """Gets the incident/marker points as JSON to be plotted on the map."""

    #Initializes empty dictionary which is then filled with the marker data
    incidents = {}
    for inc in Incident.query.all():
        lat = float(inc.latitude)
        lng = float(inc.longitude)
        incidents[inc.police_rec_num] = {
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
            "rec_number": inc.police_rec_num}

    #The marker dictionary is jsonified and sent to the google maps API through JavaScript
    return jsonify(incidents)


@app.route("/register", methods=["GET"])
def register_form():
    """Goes to registration Form."""

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
    """Registration Form."""

    """Creating empty strings in case there aren't already
                data being passed from the registration redirect"""
    fname = ""
    lname = ""
    about_me = ""

    #Sets variables equal to the form values
    email_input = request.form['email_input']
    pw_input = request.form['password'].encode('utf-8')
    username = request.form['username']
    hashed_word = bcrypt.hashpw(pw_input, bcrypt.gensalt())
    user_type = request.form['user_type']
    second_type = request.form['2nd']

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
                        user_type_secondary=second_type)
        db.session.add(new_user)
        db.session.commit()
        if user_type == "other":
            flash("""While you may enter the discussion forums if you are not a sex worker,
                   keep in mind that this website is not intended for you. Do your best to respect
                   the sex workers on this site as well as their experiences and thoughts. Also,
                   please note that pimps and human traffickers are NOT welcome on this site. This
                   site is intended for consensual sex workers working on their own
                   volition ONLY.""")
    return redirect('/login')


@app.route("/login", methods=["GET"])
def log_in():
    """Render's the log-in page if user not in session, otherwise redirects to the homepage"""
    if 'current_user' in session.keys():
        return redirect("/")
    else:
        return render_template("login.html", client_id=CLIENT_ID)


@app.route("/login", methods=["POST"])
def login():
    """Gets login info, verifies it, & either redirects to the forums or gives an error message"""

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
    """Logs user out and delets them from the session"""

    del session['current_user']

    flash('Bye! You have been succesfully logged out!')
    return redirect("/login")


@app.route("/forums")
def go_forums():
    """Renders the central forum page"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    other = Forum.query.filter_by(forum_id=7).one()

    #Checks to see if the user is logged in. If so, renders forums
    if 'current_user' in session.keys():
        return render_template("forums.html", cam=cam, dom=dom, escort=escort,
                               porn=porn, dance=dance, phone=phone, other=other)
    #Otherwise it redirects to the login page
    else:
        flash("Please login before entering the forums.")
        return redirect("/login")


@app.route("/forums/<forum_id>", methods=["POST"])
def add_post(forum_id):
    """Uses POST request to create a new post within a forum"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    other = Forum.query.filter_by(forum_id=7).one()

    #Gets the new posts content
    post_content = request.form['content']

    #Checks to see the users info and which posts they have flagged
    user = User.query.filter_by(email=session['current_user']).one()
    flag_query = Flag.query.filter(Flag.user_id == User.user_id).all()
    flags = []
    if len(flag_query) > 0:
        for item in flag_query:
            print item
            print item.post_id
            flags.append(item.post_id)

    #Adds the new post to the database
    new_post = Post(parent_post_id=0, user_id=user.user_id, username=user.username, forum_id=forum_id,
                    content=post_content, p_datetime=datetime.now(),
                    date_posted=(str(datetime.now())[:16]))

    #Doublechecks that the user isn't creating a duplicate post
    if Post.query.filter(Post.content == new_post.content,
                         Post.username == new_post.username).all() == []:
        db.session.add(new_post)
        db.session.commit()

    #Queries the post and forun data and renders everything back to the same forum page
    posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id == 0).order_by(asc(Post.post_id)).all()
    child_posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id != 0).order_by(asc(Post.post_id)).all()
    forum = Forum.query.filter_by(forum_id=forum_id).one()
    return render_template("forum_page.html", forum=forum, cam=cam, dom=dom, escort=escort,
                           porn=porn, dance=dance, phone=phone, posts=posts, 
                           child_posts=child_posts, flags=flags, other=other)


@app.route("/forums/child/<post_id>", methods=["POST"])
def add_child_post(post_id):
    """Uses POST request to create a new post within a forum"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    other = Forum.query.filter_by(forum_id=7).one()

    #Gets the new posts content
    post_content = request.form['child_content']

    #Checks to see the users info and which posts they have flagged
    user = User.query.filter_by(email=session['current_user']).one()
    flag_query = Flag.query.filter(Flag.user_id == User.user_id).all()
    flags = []
    if len(flag_query) > 0:
        for item in flag_query:
            print item
            print item.post_id
            flags.append(item.post_id)

    #Adds the new post to the database
    parent_post = Post.query.filter_by(post_id=post_id).one()
    new_post = Post(user_id=user.user_id, username=user.username, forum_id=parent_post.forum_id, parent_post_id=post_id,
                    content=post_content, p_datetime=datetime.now(),
                    date_posted=(str(datetime.now())[:16]))

    #Doublechecks that the user isn't creating a duplicate post
    if Post.query.filter(Post.content == new_post.content,
                         Post.username == new_post.username).all() == []:
        db.session.add(new_post)
        db.session.commit()

    #Queries the post and forum data and renders everything back to the same forum page
    posts = Post.query.filter(Post.forum_id == parent_post.forum_id, Post.parent_post_id == 0).order_by(asc(Post.post_id)).all()
    child_posts = Post.query.filter(Post.forum_id == parent_post.forum_id, Post.parent_post_id != 0).order_by(asc(Post.post_id)).all()
    print child_posts
    forum = Forum.query.filter_by(forum_id=posts[0].forum_id).one()
    return render_template("forum_page.html", forum=forum, cam=cam, dom=dom, escort=escort,
                           porn=porn, dance=dance, phone=phone, posts=posts, child_posts=child_posts, flags=flags, 
                           parent_post_id=post_id, other=other)


@app.route("/forums/like/<post_id>", methods=["GET"])
def add_like(post_id):
    """When the user "likes" a post, it adds it to the dbase and updates page with new like info"""

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
    return redirect("/forums/order_by_date/{}".format(forum_id))


@app.route("/forums/dislike/<post_id>", methods=["GET"])
def add_dislike(post_id):
    """When the user "dislikes" a post, it adds it to the dbase & updates page with new like info"""

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
    return redirect("/forums/order_by_date/{}".format(forum_id))


@app.route("/forums/flag/<post_id>", methods=["POST"])
def flag_post(post_id):
    """When a user submitts a flag for removal, adds it to the dbase and refreshes page"""

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
    return redirect("/forums/order_by_date/{}".format(forum_id))


@app.route("/forums/order_by_date/<forum_id>")
def date_order(forum_id):
    """Renders forum page with posts ordered by date"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    other = Forum.query.filter_by(forum_id=7).one()

    #Queries from all of the dbase tables that need to be updated and/or rendered
    posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id == 0).order_by(asc(Post.post_id)).all()
    child_posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id != 0).order_by(asc(Post.post_id)).all()
    user = User.query.filter_by(email=session['current_user']).one()
    flag_query = Flag.query.filter(Flag.user_id == User.user_id).all()
    forum = Forum.query.filter_by(forum_id=forum_id).one()

    #Defines empty flag list to be filled with user's flags
    flags = []
    if len(flag_query) > 0:
        for item in flag_query:
            print item
            print item.post_id
            flags.append(item.post_id)

    #Renders Page
    return render_template("forum_page.html", forum=forum, cam=cam, dom=dom, escort=escort,
                           porn=porn, dance=dance, phone=phone, posts=posts, 
                           child_posts=child_posts, flags=flags, flagnum=0, other=other)


@app.route("/forums/order_by_pop/<forum_id>")
def pop_order(forum_id):
    """Renders forum page with posts ordered by popularity"""

    #Defining the central forums (within app context) to be rendered
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    other = Forum.query.filter_by(forum_id=7).one()

    #Queries from all of the dbase tables that need to be updated and/or rendered
    posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id == 0).order_by(desc(Post.like_num)).all()
    child_posts = Post.query.filter(Post.forum_id == forum_id, Post.parent_post_id != 0).order_by(desc(Post.like_num)).all()
    user = User.query.filter_by(email=session['current_user']).one()
    flag_query = Flag.query.filter(Flag.user_id == User.user_id).all()
    forum = Forum.query.filter_by(forum_id=forum_id).one()

    #Defines empty flag list to be filled with user's flags
    flags = []
    if len(flag_query) > 0:
        for item in flag_query:
            print item
            print item.post_id
            flags.append(item.post_id)

    #Renders Page
    return render_template("forum_page.html", forum=forum, cam=cam, dom=dom, escort=escort,
                           porn=porn, dance=dance, phone=phone, posts=posts, 
                           child_posts=child_posts, flags=flags, flagnum=0, other=other)


@app.route("/report", methods=["GET"])
def report_page():
    """If user logged in, renders report form page, otherwise redirects to login"""

    if 'current_user' in session.keys():
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
                           fname=user.fname, lname=user.lname, about_me=user.description)



@app.route("/edit_profile", methods=["GET"])
def edit_page():
    """Renders the edit profile page"""

    user = User.query.filter_by(email=session['current_user']).one()

    return render_template("edit_profile.html", email=user.email, username=user.username,
                           fname=user.fname, lname=user.lname, about_me=user.description)



@app.route("/edit_profile", methods=["POST"])
def edit_profile():
    """Submits the profile edits"""

    #Gets info from html form and dbase
    email_input = request.form['email_input']
    pw_input = request.form['old_password']
    new_password = request.form['new_password']
    username = request.form['username']
    fname = request.form['fname']
    lname = request.form['lname']
    about_me = request.form['about_me']
    user = User.query.filter_by(email=session['current_user']).one()

    #Checks that the password matches the user's password. If so, updates the user's info
    if User.query.filter(User.email == email_input, User.password == pw_input).all() != []:
        (db.session.query(User).filter(
            User.email == session['current_user'], User.password == pw_input).update(
                {'fname': fname, 'lname': lname, 'email': email_input, 'password': new_password,
                 'username': username, 'description': about_me}))
        db.session.commit()
        flash('Your Profile was Updated!')
        return redirect("/profile")

    #Otherwise, it flashes a message and redirects to the login page
    else:
        flash('Your e-mail or password was incorrect! Please try again or Register.')
        return render_template("edit_profile.html", email=user.email, username=user.username,
                               fname=user.fname, lname=user.lname, about_me=user.description)

#####################################################

if __name__ == "__main__":
    connect_to_db(app, 'postgresql:///safework')
    print "Connected to DB."
    app.run(debug=True)
