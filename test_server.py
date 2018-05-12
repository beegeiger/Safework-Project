"""Tests for safework server.py"""
import sqlalchemy
import server
import unittest


#######################################################33

class safeworkIntegrationTestCase(unittest.TestCase):
	"""Integration tests for flask server for safework app."""

	def setUp(self):
		print "(setUp ran)"
		self.client = server.app.test_client()
		server.app.config['TESTING'] = True

	def test_homepage(self):
		result = self.client.get('/')
		self.assertIn('<h2>Welcome to SafeWork!</h2>', result.data)

	def test_map_page(self):
		result = self.client.get('/map')
		self.assertIn('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>', result.data)

	def test_incidents(self):
		result = self.client.get('incidents.json')
		self.assertIn('2011', result.data)

	# def test_reg_page(self):
	# 	result = self.client.get('incidents.json')
	# 	self.assertIn('2011', result.data)

######################################################

if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
