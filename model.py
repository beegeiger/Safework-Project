"""Models and database functions for SafeWork App"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_imageattach.entity import Image, image_attachment

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
	parent_forum_id = db.Column(db.Integer, db.ForeignKey('forums.forum_id'), nullable=True)

	def __repr__(self):
    		"""Provide helpful representation when printed."""
		return "<forum_id={} forum_name={} forum_type={} forum_desc={} created_by={} parent_forum_id={}>".format(
        	self.forum_id, self.forum_name, self.forum_type, self.forum_desc, self.created_by, self.parent_forum_id)


class Post(db.Model):
	"""Discussion Post in SafeWork App"""

	__tablename__ = "posts"

	post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	forum_id = db.Column(db.Integer, db.ForeignKey('forums.forum_id'))
	parent_post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=True)
	content = db.Column(db.String(4096))
	p_datetime = db.Column(db.DateTime, nullable=True)
	edit_datetime = db.Column(db.DateTime, nullable=True)
	like_num = db.Column(db.Integer, default=0)
	dislike_num = db.Column(db.Integer, default=0)

	def __repr__(self):
    		"""Provide helpful representation when printed."""
		return "<post_id={} user_id={} forum_id={} parent_post_id={} content={} p_datetime={} edit_datetime={} like_num={} dislike_num={}>".format(
        	self.post_id, self.user_id, self.forum_id, self.parent_post_id, self.content, self.p_datetime, self.edit_datetime, self.like_num, self.dislike_num)


class User(db.Model):
	"""Discussion Post in SafeWork App"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	password = db.Column(db.String(64))
	username = db.Column(db.String(64))
	fname = db.Column(db.String(64), nullable=True)
	lname = db.Column(db.String(64), nullable=True)
	email = db.Column(db.String(256))
	description = db.Column(db.String(512), nullable=True)
	#Image Attachment Documentation at http://sqlalchemy-imageattach.readthedocs.io/en/1.1.0/
	picture = db.Column(db.String(256), nullable=True)
	created_at = db.Column(db.DateTime, nullable=True)
	edited_at = db.Column(db.DateTime, nullable=True)

	def __repr__(self):
    		"""Provide helpful representation when printed."""
		return "<user_id={} password={} username={} fname={} lname={} email={} description={} picture={} created_at={} edited_at={}>".format(
        	self.user_id, self.password, self.username, self.fname, self.lname, self.email, self.description, self.picture, self.created_at, self.edited_at)


class Incident(db.Model):
	"""Discussion Post in SafeWork App"""

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
	time = db.Column(db.DateTime, nullable=True)
	description = db.Column(db.String(4096), nullable=True)
	police_rec_num = db.Column(db.String(256), nullable=True)
	cop_name = db.Column(db.String(256), nullable=True)
	cop_badge = db.Column(db.String(256), nullable=True)
	cop_desc = db.Column(db.String(1024), nullable=True)
	cop_pic = db.Column(db.String(256), nullable=True)
	sting_strat = db.Column(db.String(2048), nullable=True)
	avoidance = db.Column(db.String(2048), nullable=True)
	other = db.Column(db.String(2047), nullable=True)

	def __repr__(self):
    		"""Provide helpful representation when printed."""
		return "<incident_id={} police_dept_id={} source_id={} user_id={} inc_type={} latitude={} longitude={} address={} city={} state={} date={} time={} description={} police_rec_num={} cop_name={} cop_badge={} cop_desc={} cop_pic={} sting_strat={} avoidance={} other={}>".format(self.incident_id, self.police_dept_id, self.source_id, self.user_id, self.inc_type, self.latitude, self.longitude, self.address, self.city, self.state, self.date, self.time, self.description, self.police_rec_num, self.cop_name, self.cop_badge, self.cop_desc, self.cop_pic, self.sting_strat, self.avoidance, self.other)


class Police(db.Model):
	"""Discussion Forum in SafeWork App"""

	__tablename__ = "police"

	police_dept_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	name = db.Column(db.String(512))
	city = db.Column(db.String(256))
	state = db.Column(db.String(128))
	
	def __repr__(self):
    		"""Provide helpful representation when printed."""
		return "<police_dept_id={} name={} city={} state={}>".format(
        	self.police_dept_id, self.name, self.city, self.state)


class Source(db.Model):
	"""Discussion Forum in SafeWork App"""

	__tablename__ = "sources"

	source_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	s_name = db.Column(db.String(256))
	s_description = db.Column(db.String(512), nullable=True)
	url = db.Column(db.String(256), nullable=True)
	s_type =  db.Column(db.String(128), nullable=True)

	def __repr__(self):
    		"""Provide helpful representation when printed."""
		return "<source_id={} s_name={} s_description={} url={} s_type={}>".format(
        	self.source_id, self.s_name, self.s_description, self.url, self.s_type)



##############################################################################
# Helper functions

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