"""Adds data to the safework dbase"""
from model import (Forum, Post, User, Incident, Police, Source, connect_to_db, db)
import requests
from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context, jsonify, current_app)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime
import urllib
from datetime import datetime
from server import app

#######################################################
with app.app_context():
	db.drop_all()
	db.create_all()

def fill_basics():
	with app.app_context():
		police = Police(police_dept_id=1, name="User_Input")
		police2 = Police(police_dept_id=2, name="San Franciso Police Department", city="San Francisco", state="CA")
		police3 = Police(police_dept_id=3, name="Oakland Police Department", city="Oakland", state="CA")
		db.session.add(police)
		db.session.add(police2)
		db.session.add(police3)
		db.session.commit()
		source2 = Source(source_id=3, s_name="DataSF", police_dept_id=2, s_description="San Franciso Police API", url="https://data.sfgov.org/resource/cuks-n6tp.json", s_type="gov api")
		source3 = Source(source_id=2, s_name="DataSF", police_dept_id=2, s_description="San Franciso Police API", url="https://data.sfgov.org/resource/PdId.json", s_type="gov api")
		source = Source(source_id=1, s_name="User_report")
		source4 = Source(source_id=4, s_name="oaklandnet", police_dept_id=3, s_description="Oakland Police API", url="ftp://crimewatchdata.oaklandnet.com/crimePublicData.csv", s_type="gov api")
		db.session.add(source2)
		db.session.add(source3)
		db.session.add(source)
		db.session.add(source4)
		db.session.commit()
fill_basics()

def add_incident_data(source_nums):
	"""Takes a list of source_ids to collect data from"""
	with app.app_context():
		for s_num in source_nums:
			sour = Source.query.filter_by(source_id=s_num).one()
			if s_num == 2 or s_num == 3:
				incident_info = requests.get(sour.url, params = {"category": "PROSTITUTION"}).json()
			elif s_num == 4:
				raw_data = urllib.urlretrieve("ftp://crimewatchdata.oaklandnet.com/crimePublicData.csv", "oakland_data.csv")
				for row in open("oakland_data.csv"):
					incident = row.split(",")
					inc = []
					for item in incident:
						item.strip()
						inc += item
					if "PROST" in inc[3].upper():
						incident = Incident(police_dept_id=3, source_id=4, inc_type="API", address=inc[5], city="Oakland", state="CA", date=inc[1], year=inc[1][:4], time=inc[1][11:16], description=inc[3], police_rec_num=inc[2])
						db.session.add(incident)
						db.session.commit()
			for row in incident_info:
				year = int(row["date"][0:4])
				if "PROST" in row["descript"].upper() and Incident.query.filter(Incident.police_rec_num == row["incidntnum"]).all() == []:
					if year >= 2008:	
						if s_num == 3:
							incident = Incident(police_dept_id=2, source_id=3, inc_type="API", latitude=row["location"]["coordinates"][1], longitude=row["location"]["coordinates"][0], address=row["address"], city="San Francisco", state="CA", date=row["date"], year=year, time=row["time"], description=row["descript"], police_rec_num=row["incidntnum"])
							db.session.add(incident)
						elif s_num == 2:
							incident = Incident(police_dept_id=2, source_id=2, inc_type="API", latitude=row["location"]["latitude"], longitude=row["location"]["longitude"], address=row["address"], city="San Francisco", state="CA", date=row["date"], year=year, time=row["time"], description=row["descript"], police_rec_num=row["incidntnum"])
							db.session.add(incident)
						# print incident.police_rec_num
						db.session.commit()

add_incident_data([2, 3, 4])





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

