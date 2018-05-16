"""SafeWork Server"""
import json
from jinja2 import StrictUndefined
import datetime
from datetime import datetime
from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (update, desc)
from model import Forum, Post, User, Incident, Police, Source, Like, connect_to_db, db
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
    return jsonify(incidents)


@app.route("/register", methods=["GET"])
def register_form():
    """Goes to registration Form."""
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

    return redirect('/login')


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
        return redirect("/forums")
    else:
        flash('Your e-mail or password was incorrect! Please try again or Register.')
        return render_template("login.html")


@app.route("/logout")
def logout():
    del session['current_user']

    flash('Byyyyyye. You have been succesfully logged out!')
    return redirect ("/login")

# with app.app_context():
#     cam = Forum.query.filter_by(forum_id=1).one()
#     dom = Forum.query.filter_by(forum_id=2).one()
#     escort = Forum.query.filter_by(forum_id=3).one()
#     porn = Forum.query.filter_by(forum_id=4).one()
#     dance = Forum.query.filter_by(forum_id=5).one()
#     phone = Forum.query.filter_by(forum_id=6).one()



@app.route("/forums")
def go_forums():
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    if 'current_user' in session.keys():
        return render_template("forums.html", cam=cam, dom=dom, escort=escort, porn=porn, dance=dance, phone=phone)
    else:
        flash("Please login before entering the forums.")
        return redirect ("/login")


@app.route("/forums/<forum_id>", methods=["GET"])
def get_forum(forum_id):
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    posts = Post.query.filter_by(forum_id=forum_id).all()

    forum = Forum.query.filter_by(forum_id=forum_id).one()
    return render_template("forum_page.html", forum=forum, cam=cam, dom=dom, escort=escort, porn=porn, dance=dance, phone=phone, posts=posts)



@app.route("/forums/<forum_id>", methods=["POST"])
def add_post(forum_id):
    cam = Forum.query.filter_by(forum_id=1).one()
    dom = Forum.query.filter_by(forum_id=2).one()
    escort = Forum.query.filter_by(forum_id=3).one()
    porn = Forum.query.filter_by(forum_id=4).one()
    dance = Forum.query.filter_by(forum_id=5).one()
    phone = Forum.query.filter_by(forum_id=6).one()
    post_content = request.form['content']
    user = User.query.filter_by(email = session['current_user']).one()
    
    new_post = Post(user_id=user.user_id, username=user.username, forum_id=forum_id, content=post_content, p_datetime=datetime.now(), date_posted=(str(datetime.now())[:16]))
    db.session.add(new_post)
    db.session.commit()

    posts = Post.query.filter_by(forum_id=forum_id).all()

    forum = Forum.query.filter_by(forum_id=forum_id).one()
    return render_template("forum_page.html", forum=forum, cam=cam, dom=dom, escort=escort, porn=porn, dance=dance, phone=phone, posts=posts)


@app.route("/forums/like/<post_id>", methods=["GET"])
def add_like(post_id):
    user_id = User.query.filter_by(email=session['current_user']).one().user_id
    forum_id = Post.query.filter_by(post_id=post_id).one().forum_id
    like_query = Like.query.filter(Like.post_id==post_id, Like.user_id==user_id).all()
    post_query = db.session.query(Post).filter_by(post_id=post_id).one()
    if like_query == []:
        new_like = Like(user_id=user_id, post_id=post_id, like_dislike="like")
        db.session.query(Post).filter_by(post_id=post_id).update({"like_num": (post_query.like_num + 1)})
        db.session.add(new_like)
        db.session.commit()
    elif like_query[0].like_dislike == "dislike":
        db.session.query(Like).filter(Like.post_id==post_id, Like.user_id==user_id).update({"user_id": user_id, "post_id": post_id, "like_dislike": "like"})
        db.session.query(Post).filter_by(post_id=post_id).update({"like_num": (post_query.like_num + 1), "dislike_num": (post_query.dislike_num - 1)})
        db.session.commit()
    return redirect("/forums/{}".format(forum_id))


@app.route("/forums/dislike/<post_id>", methods=["GET"])
def add_dislike(post_id):
    user_id = User.query.filter_by(email=session['current_user']).one().user_id
    forum_id = Post.query.filter_by(post_id=post_id).one().forum_id
    like_query = Like.query.filter(Like.post_id==post_id, Like.user_id==user_id).all()
    post_query = db.session.query(Post).filter_by(post_id=post_id).one()
    if like_query == []:
        new_dislike = Like(user_id=user_id, post_id=post_id, like_dislike="dislike")
        db.session.query(Post).filter_by(post_id=post_id).update({"dislike_num": (post_query.dislike_num + 1)})
        db.session.add(new_dislike)
        db.session.commit()
    elif like_query[0].like_dislike == "like":
        db.session.query(Like).filter(Like.post_id==post_id, Like.user_id==user_id).update({"user_id": user_id, "post_id": post_id, "like_dislike": "dislike"})
        db.session.query(Post).filter_by(post_id=post_id).update({"dislike_num": (post_query.dislike_num + 1), "like_num": (post_query.like_num - 1)})
        db.session.commit()
    return redirect("/forums/{}".format(forum_id))



@app.route("/report", methods=["GET"])
def report_page():
    if 'current_user' in session.keys():
        return render_template("report_form.html")
    else:
        flash('You must sign in before making a report.')
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
def edit_page():
    user = User.query.filter_by(email=session['current_user']).one()

    return render_template("edit_profile.html", email=user.email, username=user.username, fname=user.fname, lname=user.lname, about_me=user.description)



@app.route("/edit_profile", methods=["POST"])
def edit_profile():
    email_input = request.form['email_input']
    pw_input = request.form['old_password']
    new_password = request.form['new_password']
    username = request.form['username']
    fname = request.form['fname']
    lname = request.form['lname']
    about_me = request.form['about_me']

    if User.query.filter(User.email == email_input, User.password == pw_input).all() != []:
        db.session.query(User).filter(User.email == session['current_user'], User.password == pw_input).update({'fname': fname, 'lname': lname, 'email': email_input, 'password': new_password, 'username': username, 'description': about_me})
        db.session.commit()
        flash('Your Profile was Updated!')
        return redirect("/profile")
    else:
        flash('Your e-mail or password was incorrect! Please try again or Register.')
        return render_template("login.html")

#####################################################

if __name__ == "__main__":
    connect_to_db(app, 'postgresql:///safework')
    print "Connected to DB."
    app.run(debug=True)