"""Get's lat/long from incidents with only address published"""
import sys
sys.path.insert(0,'..')
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
import csv
from geopy.geocoders import GoogleV3
###################################################
# def geocode(source_num):
# 	if source_num == 4:
# 		geocode_num = 0
# 		dout = []
# 		for row in open("raw_data/OaklandProst5_14.csv"):
# 			# print row
# 			geocode_num += 1
# 			while geocode_num <= 10:
# 				incident = row.split(",")
# 				inc = []
# 				address = ""
# 				for item in incident:
# 					inc += [item.translate(None, string.punctuation)]
# 				for dig in inc[5]:
# 					if dig == "/":
# 						address += "&"
# 					else:
# 						address += dig
# 				address += ", Oakland, CA"
# 				# print address
# 				API_KEY = os.getenv("GOOGLEAPI")
# 				g = GoogleV3(api_key=API_KEY)
# 				place, (lat, lng) = g.geocode(address)
# 				print [lat, lng]
# 				inc += [place, lat, lng]
# 				dout += inc
# 				# print inc
# 				print dout
# 			with open('Oakland.csv', 'wb') as fout:
# 				writer = csv.writer(fout)
# 				writer.writerows(dout)

# 			print 'all done!'				

# geocode(4)

#go to https://geocoder.ccjeng.com/ for free batch geocoder
def make_address_file():
 	dout = []
 	geocode_num = 0
	for row in open("raw_data/OaklandProst5_14.csv"):
		geocode_num += 1
		if geocode_num <= 77:
			incident = row.split(",")
			inc = []
			for item in incident:

				inc += [item.translate(None, string.punctuation)]

			address = [inc[5] + ", Oakland, CA"]
			dout += [address]
			print dout
	with open('Oakland.csv', 'wb') as fout:
		writer = csv.writer(fout)
		writer.writerows(dout)

make_address_file()