"""Models and database functions for SafeWork App"""
from flask import jsonify, Flask
import datetime
from datetime import datetime
import bcrypt
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy_imageattach.entity import Image, image_attachment

# from server import app

# Required to use Flask sessions and the debug toolbar
app = Flask(__name__)
db = SQLAlchemy()


################################################

class Forum(db.Model):
	"""Discussion Forum in SafeWork App"""

	__tablename__ = "forums"

	forum_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	forum_name = db.Column(db.String(256))
	forum_type = db.Column(db.String(64), nullable=True)
	forum_desc = db.Column(db.String(256), nullable=True)
	created_by = db.Column(db.String(128), nullable=True)
	parent_forum_id = db.Column(db.Integer, nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<forum_id={} forum_name={} forum_type={} forum_desc={} created_by={} parent_forum_id={}>".format(
			self.forum_id, self.forum_name, self.forum_type, self.forum_desc, self.created_by, self.parent_forum_id)


class Post(db.Model):
	"""Discussion Post in SafeWork App"""

	__tablename__ = "posts"

	post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	username = db.Column(db.String(64))
	forum_id = db.Column(db.Integer, db.ForeignKey('forums.forum_id'))
	parent_post_id = db.Column(db.Integer, nullable=True)
	content = db.Column(db.String(4096))
	p_datetime = db.Column(db.DateTime, nullable=True)
	edit_datetime = db.Column(db.DateTime, nullable=True)
	like_num = db.Column(db.Integer, default=0)
	dislike_num = db.Column(db.Integer, default=0)
	date_posted = db.Column(db.String(64), nullable=True)
	flag_num = db.Column(db.Integer, default=0)
	deleted = db.Column(db.Boolean, default=False)
	tagline = db.Column(db.String(100), nullable=True)
	location = db.Column(db.String(50), nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<username={} post_id={} user_id={} forum_id={} parent_post_id={} content={} p_datetime={} edit_datetime={} like_num={} dislike_num={} date_posted={} flag_num={} deleted={} tagline={} location={}>".format(
			self.username, self.post_id, self.user_id, self.forum_id, self.parent_post_id, self.content, self.p_datetime, self.edit_datetime, self.like_num, self.dislike_num, self.date_posted, self.flag_num, self.deleted, self.tagline, self.location)


class User(db.Model):
	"""User Table in SafeWork App"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_code = db.Column(db.String(4), nullable=True)
	password = db.Column(db.String(1028))
	username = db.Column(db.String(64))
	fname = db.Column(db.String(64), nullable=True)
	lname = db.Column(db.String(64), nullable=True)
	email = db.Column(db.String(256))
	email2 = db.Column(db.String(256), nullable=True)
	description = db.Column(db.String(512), nullable=True)
	#Image Attachment Documentation at http://sqlalchemy-imageattach.readthedocs.io/en/1.1.0/
	picture = db.Column(db.String(256), nullable=True)
	created_at = db.Column(db.DateTime, nullable=True)
	edited_at = db.Column(db.DateTime, nullable=True)
	user_type_main = db.Column(db.String(256), nullable=True)
	user_type_secondary = db.Column(db.String(256), nullable=True)
	tagline = db.Column(db.String(100), nullable=True)
	location = db.Column(db.String(50), nullable=True)
	user_type = db.Column(db.String(50), default="regular")
	timezone = db.Column(db.String(48))
	phone = db.Column(db.String(28), nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<user_id={} user_code={} password={} username={} fname={} lname={} email={} description={} picture={} created_at={} edited_at={} user_type_main={} user_type_secondary={}> tagline={} location={} user_type={}>".format(
			self.user_id, self.user_code, self.password, self.username, self.fname, self.lname, self.email, self.description, self.picture, self.created_at, self.edited_at, self.user_type_main, self.user_type_secondary, self.tagline, self.location, self.user_type)


class Incident(db.Model):
	"""Incidents table in SafeWork App"""

	__tablename__ = "incidents"

	incident_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	police_dept_id = db.Column(db.Integer, db.ForeignKey('police.police_dept_id'), nullable=True)
	source_id = db.Column(db.Integer, db.ForeignKey('sources.source_id'), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
	inc_type = db.Column(db.String(64), nullable=True)
	latitude = db.Column(db.String(256), nullable=True)
	longitude = db.Column(db.String(256), nullable=True)
	address = db.Column(db.String(512), nullable=True)
	city = db.Column(db.String(256), nullable=True)
	state = db.Column(db.String(256), nullable=True)
	date = db.Column(db.DateTime, nullable=True)
	year = db.Column(db.Integer, nullable=True)
	time = db.Column(db.String(256))
	description = db.Column(db.String(4096), nullable=True)
	police_rec_num = db.Column(db.String(256), nullable=False)
	sting_strat = db.Column(db.String(2048), nullable=True)
	avoidance = db.Column(db.String(2048), nullable=True)
	other = db.Column(db.String(2047), nullable=True)
	db_added_date = db.Column(db.DateTime, nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<incident_id={} police_dept_id={} source_id={} user_id={} inc_type={} latitude={} longitude={} address={} city={} state={} date={} yeardb.={} time={} description={} police_rec_num={} cop_name={} cop_badge={} cop_desc={} cop_pic={} sting_strat={} avoidance={} other={} db_added_date={}>".format(self.incident_id, self.police_dept_id, self.source_id, self.user_id, self.inc_type, self.latitude, self.longitude, self.address, self.city, self.state, self.date, self.year, self.time, self.description, self.police_rec_num, self.cop_name, self.cop_badge, self.cop_desc, self.cop_pic, self.sting_strat, self.avoidance, self.other, self.db_added_date)


class Cop(db.Model):
	"""Cop Table in SafeWork App"""

	__tablename__ = "cops"
	cop_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	police_dept_id = db.Column(db.Integer, db.ForeignKey('police.police_dept_id'), nullable=True)
	cop_name = db.Column(db.String(256), nullable=True)
	cop_badge = db.Column(db.String(256), nullable=True)
	cop_desc = db.Column(db.String(1024), nullable=True)
	cop_pic = db.Column(db.String(256), nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<cop_id={} police_dept_id={} user_id={} cop_name={} cop_badge={} cop_desc={} cop_pic={}>".format(
			self.cop_id, self.police_dept_id, self.user_id, self.cop_name, self.cop_badge, self.cop_desc, self.cop_pic)

class Police(db.Model):
	"""Police Department table in SafeWork App"""

	__tablename__ = "police"

	police_dept_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	name = db.Column(db.String(512))
	city = db.Column(db.String(256), nullable=True)
	state = db.Column(db.String(128), nullable=True)
	
	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<police_dept_id={} name={} city={} state={}>".format(
			self.police_dept_id, self.name, self.city, self.state)


class Source(db.Model):
	"""Data sources table in SafeWork App"""

	__tablename__ = "sources"

	source_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	police_dept_id = db.Column(db.Integer, db.ForeignKey('police.police_dept_id'), nullable=True)
	s_name = db.Column(db.String(256))
	s_description = db.Column(db.String(512), nullable=True)
	url = db.Column(db.String(256), nullable=True)
	s_type =  db.Column(db.String(128), nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<source_id={} s_name={} s_description={} url={} s_type={}>".format(
			self.source_id, self.s_name, self.s_description, self.url, self.s_type)

class Like(db.Model):
	"""Post Likes table in SafeWork App"""

	__tablename__ = "likes"

	like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
	like_dislike = db.Column(db.String(24))

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<like_id={} user_id={} post_id={} like_dislike={}>".format(
			self.like_id, self.user_id, self.post_id, self.like_dislike)

class Flag(db.Model):
	"""Post Dislikes table in SafeWork App"""

	__tablename__ = "flags"

	flag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
	flag_type = db.Column(db.String(24))

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<flag_id={} user_id={} post_id={} flag_type={}>".format(
			self.flag_id, self.user_id, self.post_id, self.flag_type)
 
class Contact(db.Model):
	"""SafeWalk Contacts"""

	__tablename__ = "contacts"

	contact_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	name = db.Column(db.String(96))
	email = db.Column(db.String(200), nullable=True)
	phone = db.Column(db.String(48), nullable=True)
	c_type = db.Column(db.String(48), nullable=True)
	c_message = db.Column(db.String(1028), nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<contact_id={} user_id={} name={} email={} phone={} c_type={} c_message={}>".format(
			self.contact_id, self.user_id, self.name, self.email, self.phone, self.c_type, self.c_message)

class AlertSet(db.Model):
	"""SafeWalk AlertSet"""

	__tablename__ = "alertsets"

	alert_set_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	a_name = db.Column(db.String(96))
	a_desc = db.Column(db.String(200), nullable=True)
	start_time = db.Column(db.Time, nullable=True)
	start_datetime = db.Column(db.DateTime, nullable=True)
	date = db.Column(db.Date, nullable=True)
	end_date = db.Column(db.Date, nullable=True)
	notes = db.Column(db.String(2056), nullable=True)
	interval = db.Column(db.Integer, nullable=True)
	active = db.Column(db.Boolean, default=False)
	checked_in = db.Column(db.Boolean, default=False)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<alert_set_id={} user_id={} a_name={} a_desc={} start_time={} start_datetime={} date={} end_date={} notes={} active={} checked_in={}>".format(
			self.alert_set_id, self.user_id, self.a_name, self.a_desc, self.start_time, self.start_datetime, self.date, self.end_date, self.notes, self.active, self.checked_in)

class Alert(db.Model):
	"""SafeWalk AlertSet"""

	__tablename__ = "alerts"

	alert_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	alert_set_id = db.Column(db.Integer, db.ForeignKey('alertsets.alert_set_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	contact_id1 = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'))
	contact_id2 = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'), nullable=True)
	contact_id3 = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'), nullable=True)
	active = db.Column(db.Boolean, default=False)
	sent = db.Column(db.Boolean, default=False)
	time = db.Column(db.Time, nullable=True)
	date = db.Column(db.Date, nullable=True)
	interval = db.Column(db.Integer, nullable=True)
	start_time = db.Column(db.Time, nullable=True)
	message = db.Column(db.String(1028), nullable=True)
	datetime = db.Column(db.DateTime, nullable=True)
	checked_in = db.Column(db.Boolean, default=False)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<alert_id={} alert_set_id={} user_id={} contact_id1={} contact_id2={} contact_id3={} active={} sent={} time={} date={} start_time={} message={} datetime={} checked_in={}>".format(
			self.alert_id, self.alert_set_id, self.user_id, self.contact_id1, self.contact_id2, self.contact_id3, self.active, self.sent, self.time, self.date, self.start_time, self.message, self.datetime, self.checked_in)

class CheckIn(db.Model):
	"""SafeWalk Check-Ins"""

	__tablename__ = "checkins"

	check_in_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	notes = db.Column(db.String(2056), nullable=True)
	address = db.Column(db.String(512), nullable=True)
	time = db.Column(db.Time, nullable=True)
	date = db.Column(db.Date, nullable=True)
	datetime = db.Column(db.DateTime, nullable=True)
	lat = db.Column(db.String(256), nullable=True)
	lon = db.Column(db.String(256), nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<check_in_id={} user_id={} notes={} address={} time={} date={} datetime={} lat={} lon={}>".format(
			self.check_in_id, self.user_id, self.notes, self.address, self.time, self.date, self.datetime, self.lat, self.lon)

class ReqCheck(db.Model):
	"""Required SafeWalk Check-Ins"""

	__tablename__ = "reqchecks"

	req_check_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	check_in_id = db.Column(db.Integer, db.ForeignKey('checkins.check_in_id'), nullable=True)
	alert_id = db.Column(db.Integer, db.ForeignKey('alerts.alert_id'))
	alert_set_id = db.Column(db.Integer, db.ForeignKey('alertsets.alert_set_id'))
	time = db.Column(db.Time, nullable=True)
	date = db.Column(db.Date, nullable=True)
	checked = db.Column(db.Boolean, nullable=True)


	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<req_check_id={} user_id={} check_in_id={} alert_id={} alert_set_id={} time={} date={} checked={}>".format(
			self.req_check_id, self.user_id, self.check_in_id, self.alert_id, self.alert_set_id, self.time, self.date, self.checked)

class Feedback(db.Model):
	"""Error Feedback from Users"""

	__tablename__ = "feedback"

	feedback_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	datetime = db.Column(db.DateTime, nullable=True)
	content = db.Column(db.String(2056))


	def __repr__(self):
		"""Provide helpful representation when printed."""
		return "<feedback_id={} user_id={} datetime={} content={}>".format(
			self.feedback_id, self.user_id, self.datetime, self.content)
 


################################################################################

def example_data():
	"""Example data to be used for testing."""
	#Deleting tables in case this file has been run before
	Forum.query.delete()
	Post.query.delete()
	User.query.delete()
	Incident.query.delete()
	Police.query.delete()
	Source.query.delete()
	Like.query.delete()
	Flag.query.delete()

	#Example Forum Objects
	cam = Forum(forum_id=1, forum_name="Cam Modeling", forum_type="main", forum_desc="Central Forum for all Cam Models to discuss Strategies.", created_by="dev", parent_forum_id=0)
	db.session.add(cam)	
	dom = Forum(forum_id=2, forum_name="Pro-Domination", forum_type="main", forum_desc="Central Forum for all Pro Domme's to discuss Strategies.", created_by="dev", parent_forum_id=0)
	db.session.add(dom)		
	escort = Forum(forum_id=3, forum_name="Escorting", forum_type="main", forum_desc="Central Forum for all escorts to discuss Strategies.", created_by="dev", parent_forum_id=0)
	db.session.add(escort)		
	porn = Forum(forum_id=4, forum_name="Porn", forum_type="main", forum_desc="Central Forum for all porn-makers to discuss Strategies.", created_by="dev", parent_forum_id=0)
	db.session.add(porn)		
	dance = Forum(forum_id=5, forum_name="Dancing/Stripping", forum_type="main", forum_desc="Central Forum for all dancers to discuss Strategies.", created_by="dev", parent_forum_id=0)
	db.session.add(dance)		
	phone = Forum(forum_id=6, forum_name="Phone Sex Operating", forum_type="main", forum_desc="Central Forum for all phone operators to discuss Strategies.", created_by="dev", parent_forum_id=0)
	db.session.add(phone)
	sugar = Forum(forum_id=7, forum_name="Sugaring", forum_type="main", forum_desc="Central Forum for all Sugar Babies to discuss Strategies.", created_by="dev", parent_forum_id=0)
	db.session.add(sugar)			
	other = Forum(forum_id=8, forum_name="All Other Forums", forum_type="main", forum_desc="Collection of all other discussion forums that crosscut all sex work types.", created_by="dev", parent_forum_id=0)
	db.session.add(other)
	db.session.commit()
	f1 = Forum(forum_id=9, forum_name="Example Forum Name For Testing", forum_type="main", forum_desc="Central Forum for all Cam Models to discuss Strategies.", created_by="dev", parent_forum_id=1)
	f2 = Forum(forum_id=10, forum_name="Pro-Domination", forum_type="main", forum_desc="Central Forum for all Pro Domme's to discuss Strategies.", created_by="dev", parent_forum_id=1)
	f3 = Forum(forum_id=11, forum_name="Escorting", forum_type="main", forum_desc="Central Forum for all escorts to discuss Strategies.", created_by="dev", parent_forum_id=1)

	#Example Users
	u1 = User(password=bcrypt.hashpw("12356", bcrypt.gensalt()), username="LaceyKittey", fname="Lacey", lname="Kittey", email="lkitty@.com", description="Former Escort", created_at=datetime.now(), edited_at=datetime.now())
	u2 = User(password=bcrypt.hashpw("abcdef", bcrypt.gensalt()), username="HappyDoc", fname="Happy", lname="Doc", email="HDoc@.com", description="Former Cam Model", created_at=datetime.now(), edited_at=datetime.now())
	u3 = User(password=bcrypt.hashpw("Testing", bcrypt.gensalt()), username="Testing", fname="Dev", lname="Tester", email="Testing@gmail.com", description="Former Sugar baby", created_at=datetime.now(), edited_at=datetime.now())
	
	#Example Posts
	p1 = Post(user_id=1, forum_id=1, username="LaceyKittey", content="Testing 123", p_datetime=datetime.now(), edit_datetime=datetime.now(), like_num=0, dislike_num=0)
	p2 = Post(user_id=1, forum_id=3, username="HappyDoc", content="PlumpyDopey", p_datetime=datetime.now(), edit_datetime=datetime.now(), like_num=1, dislike_num=0)

	#Example Police
	po1 = Police(police_dept_id=1, name="San Franciso Police Department", city="San Francisco", state="CA")
	po2 = Police(police_dept_id=2, name="Oakland Police Department", city="Oakland", state="CA")

	#Example Sources
	s1 = Source(source_id=2, s_name="DataSF", police_dept_id=1, s_description="San Franciso Police API", url="https://data.sfgov.org/resource/cuks-n6tp.json?$limit=50000", s_type="gov api")
	s2 = Source(source_id=1, s_name="DataSF", police_dept_id=1, s_description="San Franciso Police API", url="https://data.sfgov.org/resource/PdId.json", s_type="gov api")

	#Example Incidents
	i1 = Incident(police_dept_id=1, source_id=1, inc_type="API", latitude="33.23425", longitude="-122.124141", address="Address", city="San Francisco", state="CA", date=datetime.now(), year=2018, time="3:00", description="Prost", police_rec_num="asasdasd")
	i2 = Incident(police_dept_id=1, source_id=1, inc_type="API", latitude="33.21235", longitude="-122.123141", address="Address", city="San Francisco", state="CA", date=datetime.now(), year=2018, time="3:00", description="Prostitution Solicitation", police_rec_num="123123")
	
	#Example Likes
	l1 = Like(user_id=1, post_id=2, like_dislike="like")

	#Example Flags
	fl1 = Flag(user_id=3, post_id=1, flag_type="trolling")
	fl2 = Flag(user_id=3, post_id=2, flag_type="abusive")

	db.session.add_all([f1, f2, f3, u1, u2, u3])
	db.session.commit()
	db.session.add_all([p1, p2, po1, po2])
	db.session.commit()
	db.session.add_all([s1, s2])
	db.session.commit()
	db.session.add_all([i1, i2])
	db.session.commit()
	db.session.add_all([l1])
	db.session.commit()
	db.session.add_all([fl1, fl2])
	db.session.commit()


##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///safework'):
	"""Connect the database to our Flask app."""
	# Configure to use our PstgreSQL database
	print("Connecting")
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///safework'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.app = app
	db.init_app(app)

if __name__ == "__main__":	
	connect_to_db(app, 'postgresql:///safework')
	print("Connected to DB.")