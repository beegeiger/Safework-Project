"""Adds data to the safework dbase"""

def add_sf_data():
	sf_info = requests.get("https://data.sfgov.org/resource/cuks-n6tp.json", params = {"category": "PROSTITUTION"}).json()