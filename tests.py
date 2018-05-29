"""Tests for safework server.py"""
import sqlalchemy
import server
from unittest import TestCase
import bcrypt
from server import app
from flask import session
import unittest
from model import connect_to_db, db, example_data
from model import Forum, Post, User, Incident, Police, Source
import requests
from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (update, desc)

#######################################################33

class safeworkIntegrationTestCase(unittest.TestCase):
    """Integration tests for flask server for safework app."""

    def setUp(self):
        print "(setUp ran)"
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        """Do at end of every test."""
        
        print "(tearDown ran)"

    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn('created by and for sex workers', result.data)

    def test_map_page(self):
        result = self.client.get('/map')
        self.assertIn('<script src="/static/img/incident_map.js" async defer>', result.data)
        self.assertIn('<input id="pac-input" class="controls" type="text" placeholder="Search Box">', result.data)

    # def test_incidents(self):
    #     result = self.client.get('/incidents.json')
    #     self.assertIn('incidents', result.data)


    def test_reg_page(self):
        result = self.client.get('/register')
        self.assertIn('Please do not use your real name.', result.data)

    def test_login_page(self):
        result = self.client.get('/login')
        self.assertIn("Don't have an account?", result.data)


######################################################

class safeworkTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.drop_all()
        db.create_all()
        example_data()

    def test_registration(self):
        result = self.client.post('/register',
                                    data={"email_input": "Testing123@gmail.com", "pw_input": "Testing123", "username": "Developer", "user_type": "other"},
                                    follow_redirects=True)
        self.assertIn('While you may enter the discussion forums if you are not a sex worker', result.data)


    def test_login_failure(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email_input": "Testing@gmail.com", "pw_input": "Tawdafawvcing"},
                                  follow_redirects=True)
        self.assertIn("Your e-mail or password was incorrect!", result.data)

    def test_login_failure2(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email_input": "wefwefwef@gmail.com", "pw_input": "Tawdafawvcing"},
                                  follow_redirects=True)
        self.assertIn("There is no record of your e-mail address", result.data)

    def test_login_success(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email_input": "Testing@gmail.com", "pw_input": "Testing"},
                                  follow_redirects=True)
        self.assertIn("You were successfully logged in", result.data)

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        

##############################################################

class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'ABC'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = "Testing@gmail.com"

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.drop_all()
        db.create_all()
        example_data()

    def test_forums(self):
        result = self.client.get('/forums')
        self.assertIn('Example Forum Name For Testing', result.data)

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()

#########################################################
if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
