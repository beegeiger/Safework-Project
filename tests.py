"""Tests for safework server.py"""
import sqlalchemy
import server
from unittest import TestCase
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
        self.assertIn('<h2>Welcome to SafeWork!</h2>', result.data)

    def test_map_page(self):
        result = self.client.get('/map')
        self.assertIn('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>', result.data)

    def test_incidents(self):
        result = self.client.get('/incidents.json')
        self.assertIn('2011', result.data)

    def test_reg_page(self):
        result = self.client.get('/register')
        self.assertIn('Please do not use your real name.', result.data)



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
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_sources(self):
        """Test departments page."""

        result = self.client.get("/forums/1")
        self.assertIn("Testing 123", result.data)








#########################################################
if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
