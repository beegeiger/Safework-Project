"""Adds data to the safework dbase"""
from model import Forum, Post, User, Incident, Police, Source, connect_to_db, db
import requests
from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context, jsonify, current_app)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime
from server import app

def connect_to_db(app):
    """Connect the database to our Flask app."""
    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///safework'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."


#######################################################
db.drop_all()
db.create_all()
def add_sf_data(site, source_num):
	with app.app_context():
		police2 = Police(police_dept_id=3, name="User_Input")
		source2 = Source(source_id=3, s_name="User_report")
		db.session.add(police2)
		db.session.add(source2)
		sf_info = requests.get(site, params = {"category": "PROSTITUTION"}).json()
		if Police.query.filter_by(police_dept_id = 1).all() == []:
			police = Police(police_dept_id=1, name="San Franciso Police Department", city="San Francisco", state="CA")
			db.session.add(police)
			db.session.commit()
		if Source.query.filter_by(source_id = source_num).all() == []:
			source = Source(source_id=source_num, s_name="DataSF", s_description="San Franciso Police API", url=site, s_type="gov api")
			db.session.add(source)
			db.session.commit()
		for row in sf_info:
			year = int(row["date"][0:4])
			if "PROST" in row["descript"].upper() and Incident.query.filter(Incident.police_rec_num == row["incidntnum"]).all() == []:
				incident = Incident(police_dept_id=1, source_id=source_num, inc_type="API", latitude=row["location"]["coordinates"][1], longitude=row["location"]["coordinates"][0], address=row["address"], city="San Francisco", state="CA", date=row["date"], year=year, time=row["time"], description=row["descript"], police_rec_num=row["incidntnum"])
				db.session.add(incident)
		db.session.commit()

add_sf_data("https://data.sfgov.org/resource/cuks-n6tp.json", 1)
#add_sf_data("https://data.sfgov.org/resource/PdId.json", 2)

def add_starter_forums():
	with app.app_context():
		if Forum.query.filter_by(forum_id=1).all() == []:
			cam = Forum(forum_id=1, forum_name="Cam Modeling", forum_type="main", forum_desc="Central Forum for all Cam Models to discuss Strategies.", created_by="dev")
			db.session.add(cam)
			
			dom = Forum(forum_id=2, forum_name="Pro-Domination", forum_type="main", forum_desc="Central Forum for all Pro Domme's to discuss Strategies.", created_by="dev")
			db.session.add(dom)
			
			escort = Forum(forum_id=3, forum_name="Escorting", forum_type="main", forum_desc="Central Forum for all escorts to discuss Strategies.", created_by="dev")
			db.session.add(escort)
			
			porn = Forum(forum_id=4, forum_name="Porn", forum_type="main", forum_desc="Central Forum for all porn-makers to discuss Strategies.", created_by="dev")
			db.session.add(porn)
			
			dance = Forum(forum_id=5, forum_name="Dancing/Stripping", forum_type="main", forum_desc="Central Forum for all dancers to discuss Strategies.", created_by="dev")
			db.session.add(dance)
			
			phone = Forum(forum_id=6, forum_name="Phone Sex Operating", forum_type="main", forum_desc="Central Forum for all phone operators to discuss Strategies.", created_by="dev")
			db.session.add(phone)
			
			other = Forum(forum_id=7, forum_name="All Other Forums", forum_type="main", forum_desc="Collection of all other discussion forums.", created_by="dev")
			db.session.add(other)

			db.session.commit()

add_starter_forums()
##############################################


