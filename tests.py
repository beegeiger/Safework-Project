"""Tests for safework server.py"""
import sqlalchemy
import server
import unittest
from model import connect_to_db, db, example_data
from model import Forum, Post, User, Incident, Police, Source

#######################################################33

class safeworkIntegrationTestCase(unittest.TestCase):
	"""Integration tests for flask server for safework app."""

	def setUp(self):
		print "(setUp ran)"
		self.client = server.app.test_client()
		server.app.config['TESTING'] = True
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()
        example_data()

	def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()

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
		result = self.client.get('/register', methods=["GET"])
		self.assertIn('2011', result.data)



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

        result = Source.query.filter_by(source_id=1).one()
        self.assertIn("Legal", result)

    def test_departments_details(self):
        """Test departments page."""

        result = self.client.get("/department/fin")
        self.assertIn("Phone: 555-1000", result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"user_id": "rachel", "password": "123"},
                                  follow_redirects=True)
        self.assertIn("You are a valued user", result.data)








#########################################################
if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
