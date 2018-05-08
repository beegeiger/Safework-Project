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
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

#######################################################
db.drop_all()
db.create_all()
def add_sf_data(site, source_num):
	with app.app_context():
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
				incident = Incident(police_dept_id=1, source_id=source_num, inc_type="API", latitude=row["location"]["coordinates"][0], longitude=row["location"]["coordinates"][1], address=row["address"], city="San Francisco", state="CA", date=row["date"], time=row["time"], description=row["descript"], police_rec_num=row["incidntnum"])
				db.session.add(incident)
		db.session.commit()

add_sf_data("https://data.sfgov.org/resource/cuks-n6tp.json", 1)
#add_sf_data("https://data.sfgov.org/resource/PdId.json", 2)

##############################################


