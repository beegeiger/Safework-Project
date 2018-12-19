"""Tests for safework server.py"""
import sqlalchemy
import server
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
        print("setUp ran")
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        """Do at end of every test."""
        
        print("tearDown ran")

    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn('created by and for sex workers', result.data)

    def test_map_page(self):
        result = self.client.get('/map')
        self.assertIn('<input id="PointscheckBox" type="checkbox" checked>', result.data)
        self.assertIn('<div id="floating-panel" width=100%>', result.data)

    # def test_incidents(self):
    #     result = self.client.get('/incidents.json')
    #     self.assertIn('incidents', result.data)


    def test_reg_page(self):
        result = self.client.get('/register')
        self.assertIn('Please do not use your real name.', result.data)

    def test_login_page(self):
        result = self.client.get('/login')
        self.assertIn("Don't have an account?", result.data)

    def test_resources_page(self):
        result = self.client.get('/resources')
        self.assertIn("St. James Infirmiry", result.data)

    def test_contact_page(self):
        result = self.client.get('/contact')
        self.assertIn("E-mail safeworkapp@gmail.com with any comments!", result.data)




######################################################

class safeworkTestsDatabase(unittest.TestCase):
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

    # def test_registration(self):
    #     """Testing Registration"""
    #     result = self.client.post("/register",
    #                               data={"email_input": "Testing1234@gmail.com", "password": "Testing123", "username": "Developer", "user_type": "other", "2nd": "support", "fname": "Happy", "lname": "Dopey", "about_me": "Doc"},
    #                               follow_redirects=True)
    #     self.assertIn("While you may enter the discussion forums if you are not a sex worker", result.data)
    #     result = self.client.post('/login',
    #                               data={"email_input": "Testing1234@gmail.com", "pw_input": "Testing123"},
    #                               follow_redirects=True)
    #     self.assertIn('You were successfully logged in', result.data)


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

class FlaskTestsLoggedIn(unittest.TestCase):
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

    def test_add_post(self):
        result = self.client.post('/forums/parent/1/1',
                                    data={"content": "Test Post Content for Testing9876543"},
                                    follow_redirects=True)
        self.assertIn("Test Post Content for Testing9876543", result.data)
        self.assertIn("Central Forum for all Cam Models to discuss Strategies", result.data)
        
    def test_add_child_post(self):
        self.client.post('/forums/parent/1/1',
                                    data={"content": "Test Post Content for Testing9876543"},
                                    follow_redirects=True)
        p_post = Post.query.filter_by(content="Test Post Content for Testing9876543").one()
        result = self.client.post('/forums/child/' + str(p_post.post_id),
                                    data={"child_content": "Test Post Content for Testing ABC 876", "parent_post_id": p_post.post_id},
                                    follow_redirects=True)
        self.assertIn("Test Post Content for Testing ABC 876", result.data)

    def test_edit_post(self):
        result = self.client.post('/forums/parent/1/1',
                                    data={"content": "Test Post Content for Testing9876543"},
                                    follow_redirects=True)
        result = self.client.post('/forums/edit/3',
                                    data={"child_content": "Edited Post12345 for Testing"},
                                    follow_redirects=True)
        self.assertIn("Edited Post12345 for Testing", result.data)
        
    def test_delete_post(self):
        result = self.client.post('/forums/parent/1/1',
                                    data={"content": "Test Post Content for Testing9876543"},
                                    follow_redirects=True)
        result = self.client.post('/forums/delete/3',
                                    data={"delete_check": "Yes"},
                                    follow_redirects=True)
        self.assertNotIn("Edited Post12345 for Testing", result.data)

    def test_like_post(self):
        result = self.client.post('/forums/parent/1/1',
                                  data={"content": "Test Post Content for Testing9876543"},
                                  follow_redirects=True)
        result = self.client.get('/forums/like/3',
                                   follow_redirects=True)
        self.assertIn('<a href="/forums/like/3">Like</a>(1)', result.data)

    def test_dislike_post(self):
        self.client.post('/forums/parent/1/1',
                                  data={"content": "Test Post Content for Testing9876543"},
                                  follow_redirects=True)
        result = self.client.get('/forums/dislike/3',
                                   follow_redirects=True)
        self.assertIn('<a href="/forums/dislike/3">Dislike</a>(1)', result.data)

    def test_flag_post(self):
        self.client.post('/forums/parent/1/1',
                                  data={"content": "Test Post Content for Testing9876543"},
                                  follow_redirects=True)
        result = self.client.post('/forums/flag/3',
                                    data={'flag_rad': 'trolling'},
                                   follow_redirects=True)
        self.assertIn('Your report has been submitted!', result.data)

    def test_date_order(self):
        """Tests that the page load, but doesn't test the actual post order (yet)"""
        self.client.post('/forums/parent/1/1',
                                  data={"content": "Test Post Content for Testing12412424"},
                                  follow_redirects=True)
        result = self.client.get('/forums/order_by_date/1/1',
                                   follow_redirects=True)
        self.assertIn("Test Post Content for Testing12412424", result.data)

    def test_pop_order(self):
        """Tests that the page load, but doesn't test the actual post order (yet)"""
        self.client.post('/forums/parent/1/1',
                                  data={"content": "Test Post Content for Testing090980987"},
                                  follow_redirects=True)
        result = self.client.get('/forums/order_by_pop/1/1',
                                   follow_redirects=True)
        self.assertIn("Test Post Content for Testing090980987", result.data)

    def test_logout(self):
        result = self.client.get('/logout',
                                  follow_redirects=True)
        self.assertIn('Bye! You have been succesfully logged out!', result.data)

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()

#########################################################
if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
