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
import string
import os
from geopy import geocoders

connect_to_db(app, 'postgresql:///safework')
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
		source2 = Source(source_id=3, s_name="DataSF", police_dept_id=2, s_description="San Franciso Police API", url="https://data.sfgov.org/resource/cuks-n6tp.json?$limit=50000", s_type="gov api")
		# source3 = Source(source_id=2, s_name="DataSF", police_dept_id=2, s_description="San Franciso Police API", url="https://data.sfgov.org/resource/PdId.json", s_type="gov api")
		source = Source(source_id=1, s_name="User_report")
		source4 = Source(source_id=4, s_name="oaklandnet_90_days", police_dept_id=3, s_description="Oakland Police API Last 90 Days", url="ftp://crimewatchdata.oaklandnet.com/crimePublicData.csv", s_type="gov api")
		# source5 = Source(source_id=5, s_name="oaklandnet_2015", police_dept_id=3, s_description="Oakland Police API 2015", url="https://data.oaklandnet.com/resource/b6ww-9zsp.json", s_type="gov api")
		db.session.add(source2)
		# db.session.add(source3)
		db.session.add(source)
		db.session.add(source4)
		db.session.commit()
fill_basics()

#Used Syntax from https://gis.stackexchange.com/questions/22108/how-to-geocode-300-000-addresses-on-the-fly
def geocode(address):
    g = geocoders.GoogleV3()
    place, (lat, lng) = g.geocode(address)
    return [lat, lng]

parameters = [{"category": "PROSTITUTION"}]
# , "dayofweek": "Monday"}, {"category": "PROSTITUTION", "dayofweek": "Tuesday"}, {"category": "PROSTITUTION", "dayofweek": "Wednesday"}, {"category": "PROSTITUTION", "dayofweek": "Thursday"}, {"category": "PROSTITUTION", "dayofweek": "Friday"}, {"category": "PROSTITUTION", "dayofweek": "Saturday"}, {"category": "PROSTITUTION", "dayofweek": "Sunday"}]


def add_incident_data(source_nums):
	"""Takes a list of source_ids to collect data from"""
	with app.app_context():
		for s_num in source_nums:
			sour = Source.query.filter_by(source_id=s_num).one()
			sf_num = 0	
			if s_num == 2 or s_num == 3:
				incident_info = requests.get(sour.url, params={"category": "PROSTITUTION"}).json()
				for row in incident_info:
					sf_num += 1
					print "sf # " + str(sf_num)
					print row
					year = int(row["date"][0:4])
					if "PROST" in row["descript"].upper() and Incident.query.filter(Incident.police_rec_num == row["incidntnum"]).all() == []:
						if year >= 2008:	
							if s_num == 3:
								incident = Incident(police_dept_id=2, source_id=3, inc_type="API", latitude=row["location"]["coordinates"][1], longitude=row["location"]["coordinates"][0], address=row["address"], city="San Francisco", state="CA", date=row["date"], year=year, time=row["time"], description=row["descript"], police_rec_num=row["incidntnum"])
								db.session.add(incident)
							elif s_num == 2:
								incident = Incident(police_dept_id=2, source_id=2, inc_type="API", latitude=row["location"]["latitude"], longitude=row["location"]["longitude"], address=row["address"], city="San Francisco", state="CA", date=row["date"], year=year, time=row["time"], description=row["descript"], police_rec_num=row["incidntnum"])
								db.session.add(incident)
							 	print incident.latitude, incident.longitude
							 	print type(incident.latitude), type(incident.longitude)
						db.session.commit()
			elif s_num == 4:
				o_num = 0
				for row in open("seed_data/oaklandcoords.csv"):
					o_num += 1
					print "Oakland # " + str(o_num)
					incident_row = row.split(",")
					# print incident[-2], incident[-1]
					inc = []
					item_num = 0
					for item in incident_row:
						item_num += 1
						if item_num <=10:
							inc += [item.translate(None, string.punctuation)]
						else:
							inc += item
					address = str(inc[5])
					incident = Incident(police_dept_id=3, source_id=4, inc_type="API", address=address, latitude=unicode(incident_row[-2].strip(), "utf-8"), longitude=unicode(incident_row[-1].strip(), "utf-8"), city="Oakland", state="CA", date=inc[1], year=inc[1][:4], time=inc[1][11:16], description=inc[3], police_rec_num=inc[2])
					db.session.add(incident)
					print incident.latitude, incident.longitude
					print type(incident.latitude), type(incident.longitude)
					db.session.commit()
				

add_incident_data([3, 4])





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


if __name__ == "__main__":

	connect_to_db(app, 'postgresql:///safework')
	print "Connected to DB."

