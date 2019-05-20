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
import flask_testing


#######################################################33

# class safeworkIntegrationTestCase(unittest.TestCase):
#     """Integration tests for flask server for safework app."""

#     def setUp(self):
#         print("setUp ran")
#         self.client = server.app.test_client()
#         server.app.config['TESTING'] = True

#     def tearDown(self):
#         """Do at end of every test."""
        
#         print("tearDown ran")

#     def test_homepage(self):
#         result = self.client.get('/')
#         self.assertIn('created by and for sex workers'.encode(), result.data)

#     def test_map_page(self):
#         result = self.client.get('/map')
#         self.assertIn('<input id="PointscheckBox" type="checkbox" checked>'.encode(), result.data)

#     # def test_incidents(self):
#     #     result = self.client.get('/incidents.json')
#     #     self.assertIn('incidents', result.data)


#     def test_reg_page(self):
#         result = self.client.get('/register')
#         self.assertIn('Feel free to use any name, real or fake!'.encode(), result.data)

#     def test_login_page(self):
#         result = self.client.get('/login')
#         self.assertIn("Don't have an account?".encode(), result.data)

#     def test_resources_page(self):
#         result = self.client.get('/resources')
#         self.assertIn("St. James Infirmiry".encode(), result.data)

#     def test_contact_page(self):
#         result = self.client.get('/contact')
#         self.assertIn("E-mail safeworkapp@gmail.com with any comments!".encode(), result.data)




######################################################

# class safeworkTestsDatabase(unittest.TestCase):
#     """Flask tests that use the database."""
#     # db = SQLAlchemy()
#     # db.app = app
#     # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'
#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'ABC'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['current_user'] = "Testing@gmail.com"



#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data

#         db.drop_all()
#         db.create_all()
#         example_data()

#     # def test_registration(self):
#     #     """Testing Registration"""
#     #     result = self.client.post("/register",
#     #                               data={"email_input": "Testing1234@gmail.com", "password": "Testing123", "username": "Developer", "user_type": "other", "2nd": "support", "fname": "Happy", "lname": "Dopey", "about_me": "Doc"},
#     #                               follow_redirects=True)
#     #     self.assertIn("While you may enter the discussion forums if you are not a sex worker", result.data)
#     #     result = self.client.post('/login',
#     #                               data={"email_input": "Testing1234@gmail.com", "pw_input": "Testing123"},
#     #                               follow_redirects=True)
#     #     self.assertIn('You were successfully logged in', result.data)


#     def test_login_failure(self):
#         """Test login page."""

#         result = self.client.post("/login",
#                                   data={"email_input": "Testing@gmail.com".encode(), "pw_input": "Tawdafawvcing".encode()},
#                                   follow_redirects=True)
#         self.assertIn("Your e-mail or password was incorrect!".encode(), result.data)

#     def test_login_failure2(self):
#         """Test login page."""

#         result = self.client.post("/login",
#                                   data={"email_input": "wefwefwef@gmail.com", "pw_input": "Tawdafawvcing"},
#                                   follow_redirects=True)
#         self.assertIn("There is no record of your e-mail address".encode(), result.data)

#     def test_login_success(self):
#         """Test login page."""

#         result = self.client.post("/login",
#                                   data={"email_input": "Testing@gmail.com", "pw_input": "Testing"},
#                                   follow_redirects=True)
#         self.assertIn("You were successfully logged in".encode(), result.data)

#     def tearDown(self):
#         """Do at end of every test."""
#         db.session.close()
    

# ##############################################################

# class FlaskTestsLoggedIn(unittest.TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'ABC'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['current_user'] = "Testing@gmail.com"



#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data

#         db.drop_all()
#         db.create_all()
#         example_data()

#     def test_forums(self):
#         result = self.client.get('/forums')
#         self.assertIn('Example Forum Name For Testing', str(result.data))

#     def test_add_post(self):
#         result = self.client.post('/forums/parent/1/1',
#                                     data={"content": "Test Post Content for Testing9876543"},
#                                     follow_redirects=True)
#         self.assertIn("Test Post Content for Testing9876543", str(result.data))
#         self.assertIn("Central Forum for all Cam Models to discuss Strategies", str(result.data))
        
#     def test_add_child_post(self):
#         self.client.post('/forums/parent/1/1',
#                                     data={"content": "Test Post Content for Testing9876543"},
#                                     follow_redirects=True)
#         p_post = Post.query.filter_by(content="Test Post Content for Testing9876543").one()
#         result = self.client.post('/forums/child/' + str(p_post.post_id),
#                                     data={"child_content": "Test Post Content for Testing ABC 876", "parent_post_id": p_post.post_id},
#                                     follow_redirects=True)
#         self.assertIn("Test Post Content for Testing ABC 876", str(result.data))

#     def test_edit_post(self):
#         result = self.client.post('/forums/parent/1/1',
#                                     data={"content": "Test Post Content for Testing9876543"},
#                                     follow_redirects=True)
#         result = self.client.post('/forums/edit/3',
#                                     data={"child_content": "Edited Post12345 for Testing"},
#                                     follow_redirects=True)
#         self.assertIn("Edited Post12345 for Testing", str(result.data))
        
#     def test_delete_post(self):
#         result = self.client.post('/forums/parent/1/1',
#                                     data={"content": "Test Post Content for Testing9876543"},
#                                     follow_redirects=True)
#         result = self.client.post('/forums/delete/3',
#                                     data={"delete_check": "Yes"},
#                                     follow_redirects=True)
#         self.assertNotIn("Edited Post12345 for Testing", str(result.data))

#     def test_like_post(self):
#         result = self.client.post('/forums/parent/1/1',
#                                   data={"content": "Test Post Content for Testing9876543"},
#                                   follow_redirects=True)
#         result = self.client.get('/forums/like/3',
#                                    follow_redirects=True)
#         self.assertIn('<a href="/forums/like/3">Like</a>(1)', str(result.data))

#     def test_dislike_post(self):
#         self.client.post('/forums/parent/1/1',
#                                   data={"content": "Test Post Content for Testing9876543"},
#                                   follow_redirects=True)
#         result = self.client.get('/forums/dislike/3',
#                                    follow_redirects=True)
#         self.assertIn('<a href="/forums/dislike/3">Dislike</a>(1)', str(result.data))

#     def test_flag_post(self):
#         self.client.post('/forums/parent/1/1',
#                                   data={"content": "Test Post Content for Testing9876543"},
#                                   follow_redirects=True)
#         result = self.client.post('/forums/flag/3',
#                                     data={'flag_rad': 'trolling'},
#                                    follow_redirects=True)
#         self.assertIn('Your report has been submitted!', str(result.data))

#     def test_date_order(self):
#         """Tests that the page load, but doesn't test the actual post order (yet)"""
#         self.client.post('/forums/parent/1/1',
#                                   data={"content": "Test Post Content for Testing12412424"},
#                                   follow_redirects=True)
#         result = self.client.get('/forums/order_by_date/1/1',
#                                    follow_redirects=True)
#         self.assertIn("Test Post Content for Testing12412424", str(result.data))

#     def test_pop_order(self):
#         """Tests that the page load, but doesn't test the actual post order (yet)"""
#         self.client.post('/forums/parent/1/1',
#                                   data={"content": "Test Post Content for Testing090980987"},
#                                   follow_redirects=True)
#         result = self.client.get('/forums/order_by_pop/1/1',
#                                    follow_redirects=True)
#         self.assertIn("Test Post Content for Testing090980987", str(result.data))

#     def test_logout(self):
#         result = self.client.get('/logout',
#                                   follow_redirects=True)
#         self.assertIn('Bye! You have been succesfully logged out!', str(result.data))

#     def tearDown(self):
#         """Do at end of every test."""
#         db.session.close()


#########################################################

class FlaskTestsSafeWalk(unittest.TestCase):
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

    def test_sw_main(self):
        """Tests that the main Safewalk Page Loads."""
        result = self.client.get('/sw_main')
        self.assertIn('Press this Button to Generate a New Code.', str(result.data))

    def test_sw_gettingstarted(self):
        """Tests that the Safewalk Getting Started Page Loads."""
        result = self.client.get('/sw_getting_started')
        self.assertIn('A scheduled alert-set allows you to pre-set alerts(/check-in requirements) by time.', str(result.data))

    def test_rec_alerts(self):
        """Tests that the recurring alerts page loads."""
        result = self.client.get('/rec_alerts')
        self.assertIn('How often would you like to require checking in with the app?', str(result.data))    

    def test_sched_alerts(self):
        result = self.client.get('/sched_alerts')
        self.assertIn('What would you like to name this alert set?', str(result.data)) 





    def test_contacts(self):
        result = self.client.get('/contacts')
        self.assertIn('Custom Message For Contact', str(result.data))   

    def test_edit_rec(self):
        result = self.client.get('/edit_recset/2')
        self.assertIn('How often would you like to require checking in with the app?', str(result.data))

    def test_edit_sched(self):
        result = self.client.get('/edit_schedset/1')
        self.assertIn('Where are you going and/or what are you doing that you might need this alert?', str(result.data))
    
    def test_check_ins(self):
        """Still needs work"""
        result = self.client.get('/check_ins')
        self.assertIn('Include a short message about where you are, if you are safe, and/or what your plans are:', str(result.data))

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()





##########################################################
if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
