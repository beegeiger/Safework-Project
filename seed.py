"""Adds data to the safework dbase"""
from model import Forum, Post, User, Incident, Police, Source, connect_to_db, db
import requests
from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from server import app

#######################################################


def add_sf_data():
	sf_info = requests.get("https://data.sfgov.org/resource/cuks-n6tp.json", params = {"category": "PROSTITUTION"}).json()
	for row in sf_info:
		incident = Incident(police_dept_id=1, source_id=1, inc_type="API", latitude=row["location"]["coordinates"][0], longitude=row["location"]["coordinates"][1], address=row["address"], city="San Francisco", state="CA", date=row["date"], time=["time"], description=row["descript"], police_rec_num=row["incidntnum"])
		db.session.add(incident)
	db.session.commit()

add_sf_data()

