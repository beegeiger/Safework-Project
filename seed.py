"""Adds data to the safework dbase"""
from model import (Forum, Post, User, Incident, Police, Source, Like, Flag, connect_to_db, db)
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

from server import app

connect_to_db(app, 'postgresql:///safework')
#######################################################
with app.app_context():
 	db.drop_all()
 	db.create_all()

def fill_basics():
	with app.app_context():
		Police1 = Police(police_dept_id=1, name="User_Input")
		Police2 = Police(police_dept_id=2, name="San Franciso Police Department", city="San Francisco", state="CA")
		Police3 = Police(police_dept_id=3, name="Oakland Police Department", city="Oakland", state="CA")
		Police4 = Police(police_dept_id=4, name="Alameda County Sheriff's Department", city="Oakland", state="CA")
		Police5 = Police(police_dept_id=5, name="Santa Clara County Sheriff's Office", city="San Jose", state="CA")
		Police6 = Police(police_dept_id=6, name="Fremont Police Department", city="Fremont", state="CA")
		Police7 = Police(police_dept_id=7, name="San Leandro Police Department", city="San Leandro", state="CA")
		Police8 = Police(police_dept_id=8, name="San Pablo Police Department", city="San Pablo", state="CA")
		Police9 = Police(police_dept_id=9, name="New York Police Department", city="New York", state="NY")
		user = User(password="Test123", username="Test123", fname="Test123", lname="Test123", email="Test123@gmail.com", description="Former Escort", created_at=datetime.now(), edited_at=datetime.now())
		db.session.add_all([Police1, Police2, Police3, Police4, Police5, Police6, Police7, Police8, Police9, user])
		db.session.commit()
		source2 = Source(source_id=3, s_name="DataSF", police_dept_id=2, s_description="San Franciso Police API", url="https://data.sfgov.org/resource/cuks-n6tp.json?$limit=50000", s_type="gov api")
		source3 = Source(source_id=2, s_name="DataSF", police_dept_id=2, s_description="San Franciso Police API", url="https://data.sfgov.org/resource/PdId.json", s_type="gov api")
		source = Source(source_id=1, s_name="User_report")
		source4 = Source(source_id=4, s_name="oaklandnet_90_days", police_dept_id=3, s_description="Oakland Police API Last 90 Days", url="ftp://crimewatchdata.oaklandnet.com/crimePublicData.csv", s_type="gov api")
		source5 = Source(source_id=5, s_name="socrata", police_dept_id=4, s_description="Alameda County Sheriff's Department API", url="https://moto.data.socrata.com/resource/bvi2-5rde.json?$where=incident_description%20like%20%27%25PROST%25%27", s_type="gov api")
		source6 = Source(source_id=6, s_name="socrata", police_dept_id=5, s_description="Santa Clara County Sheriff's Office API", url="https://moto.data.socrata.com/resource/wrmr-tdyp.json?$where=incident_description%20like%20%27%25PROST%25%27", s_type="gov api")
		source7 = Source(source_id=7, s_name="socrata", police_dept_id=6, s_description="FPD API", url="https://moto.data.socrata.com/resource/nnzs-rxi5.json?$where=incident_description%20like%20%27%25PROST%25%27", s_type="gov api")
		source8 = Source(source_id=8, s_name="socrata", police_dept_id=7, s_description="SLPD API", url="https://moto.data.socrata.com/resource/6nbc-apvm.json?$where=incident_description%20like%20%27%25PROST%25%27", s_type="gov api")
		source9 = Source(source_id=9, s_name="socrata", police_dept_id=8, s_description="SPPD API", url="https://moto.data.socrata.com/resource/tsdt-igxn.json?$where=incident_description%20like%20%27%25PROST%25%27", s_type="gov api")
		source10 = Source(source_id=10, s_name="socrata", police_dept_id=9, s_description="NYPD Socrata API Recent Data", url="https://data.cityofnewyork.us/resource/7x9x-zpz6.json?$where=pd_desc%20like%20%27%25PROST%25%27", s_type="gov api")
		source11 = Source(source_id=11, s_name="socrata", police_dept_id=9, s_description="NYPD Socrata API Historic Data", url="https://data.cityofnewyork.us/resource/9s4h-37hy.json?$where=pd_desc%20like%20%27%25PROST%25%27&$limit=50000", s_type="gov api")
		db.session.add_all([source2, source3, source4, source5, source6, source7, source8, source9, source10, source11])
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
			new_york = 0
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
			elif s_num == 5:
				incident_info = requests.get(sour.url).json()
				alameda = 0
				for row in incident_info:
					alameda += 1
					print "Alameda" + str(alameda)
					print row
					year = int(row["incident_datetime"][0:4])
					if Incident.query.filter(Incident.police_rec_num == row["incident_id"]).all() == []:
						if year >= 2008:	
								incident = Incident(police_dept_id=4, source_id=5, inc_type="API", latitude=row["latitude"], longitude=row["longitude"], address=row["address_1"], city=row["city"], state="CA", date=row["incident_datetime"], year=year, time=(str(row["hour_of_day"]) + ":00"), description=row["incident_description"], police_rec_num=row["incident_id"])
								db.session.add(incident)
						db.session.commit()
			elif s_num == 6:
				incident_info = requests.get(sour.url).json()
				santa_clara = 0
				for row in incident_info:
					santa_clara += 1
					print "Santa Clara " + str(santa_clara)
					print row
					year = int(row["incident_datetime"][0:4])
					if Incident.query.filter(Incident.police_rec_num == row["incident_id"]).all() == []:
						if year >= 2008:	
								incident = Incident(police_dept_id=5, source_id=6, inc_type="API", latitude=row["latitude"], longitude=row["longitude"], address=row["address_1"], city=row["city"], state="CA", date=row["incident_datetime"], year=year, time=(str(row["hour_of_day"]) + ":00"), description=row["incident_description"], police_rec_num=row["incident_id"])
								db.session.add(incident)
						db.session.commit()
			elif s_num == 7:
				incident_info = requests.get(sour.url).json()
				fremont = 0
				for row in incident_info:
					fremont += 1
					print "Fremont " + str(fremont)
					print row
					year = int(row["incident_datetime"][0:4])
					if Incident.query.filter(Incident.police_rec_num == row["incident_id"]).all() == []:
						if year >= 2008:	
								incident = Incident(police_dept_id=6, source_id=7, inc_type="API", latitude=row["latitude"], longitude=row["longitude"], address=row["address_1"], city=row["city"], state="CA", date=row["incident_datetime"], year=year, time=(str(row["hour_of_day"]) + ":00"), description=row["incident_description"], police_rec_num=row["incident_id"])
								db.session.add(incident)
						db.session.commit()
			elif s_num == 8:
				incident_info = requests.get(sour.url).json()
				san_leandro = 0
				for row in incident_info:
					san_leandro+= 1
					print "San Leandro " + str(san_leandro)
					print row
					year = int(row["incident_datetime"][0:4])
					if Incident.query.filter(Incident.police_rec_num == row["incident_id"]).all() == []:
						if year >= 2008:	
								incident = Incident(police_dept_id=7, source_id=8, inc_type="API", latitude=row["latitude"], longitude=row["longitude"], address=row["address_1"], city=row["city"], state="CA", date=row["incident_datetime"], year=year, time=(str(row["hour_of_day"]) + ":00"), description=row["incident_description"], police_rec_num=row["incident_id"])
								db.session.add(incident)
						db.session.commit()
			elif s_num == 9:
				incident_info = requests.get(sour.url).json()
				san_pablo = 0
				for row in incident_info:
					san_pablo += 1
					print "San Pablo " + str(san_pablo)
					print row
					year = int(row["incident_datetime"][0:4])
					if Incident.query.filter(Incident.police_rec_num == row["incident_id"]).all() == []:
						if year >= 2008:	
								incident = Incident(police_dept_id=8, source_id=9, inc_type="API", latitude=row["latitude"], longitude=row["longitude"], address=row["address_1"], city=row["city"], state="CA", date=row["incident_datetime"], year=year, time=(str(row["hour_of_day"]) + ":00"), description=row["incident_description"], police_rec_num=row["incident_id"])
								db.session.add(incident)
						db.session.commit()
			elif s_num == 10 or s_num == 11:
				incident_info = requests.get(sour.url).json()
				inde = 0
				for row in incident_info:
					new_york += 1
					inde += 1
					print "New York " + str(new_york)
					print row
					year = int(row["cmplnt_fr_dt"][0:4])
					if Incident.query.filter(Incident.police_rec_num == row["cmplnt_num"]).all() == [] and "latitude" in row:
						if year >= 2008:	
								incident = Incident(police_dept_id=9, source_id=s_num, inc_type="API", latitude=row["latitude"], longitude=row["longitude"], address=row["boro_nm"], city="New York", state="CA", date=row["cmplnt_fr_dt"], year=year, time=(str(row["cmplnt_fr_tm"])), description=row["pd_desc"], police_rec_num=row["cmplnt_num"])
								db.session.add(incident)
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
					print type(incident.latitude)
					db.session.commit()
				

add_incident_data([3, 4, 5, 6, 7, 8, 9, 10, 11])





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

