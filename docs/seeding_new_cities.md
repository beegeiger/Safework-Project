# Seeding New Cities to the SafeWork Project Database
## Currently Supported Cities/Areas
- San Francisco, CA; In-depth relevant historical incident records

- Alameda County, CA (which includes Oakland); Some historical incidents. In depth records for the past 90 days.

- Santa Clara County, CA (which includes San Jose); Extremely sporatic and limited data

- Other Bay Area cities (Fremont, San Pablo, San Leandro); Some data, but not at all complete

- New York City, NY; Good amount of data, but it doesn't go back very far and its not at all comprehensive given NYC's population and history 

## Cities to be Added
### These cities are a priority to be added soon (the data may or may not be available):
- Los Angeles, CA

- Chicago, IL

- Houston, TX

- Atlanta, GA

- Washington DC

- Detroit, MI

- New Orleans, LA

- Philidelphia, PA

- St. Louis, MO

## Finding the Appropriate City's Crime Data
- Only certain places in the country publish data that can be used in the SafeWork Project.

	- Even though Nevada has the highest sex work arrest rate per capita, as far as we can tell, they don't publish the individual incident reports.

	- In the Bay Area, San Francisco has in-depth historical incident data published going back to 2004. Alameda county has some historical incidents published, but always has the last 90 days' incidents published. Otherwise, the municipalities in the area are sporatic at best. This is the most typical.

- Start by googling the city you are looking for plus "crime incident data", "incident reports", etc.
	
	- There are a few other Crime API's (particularly through individual cities' sites) that publish data, but most is located in the Socrata Database

- Once you find an API containing incident data, look at the data.

	- Do a ctrl+F search for "PROST." If nothing comes up, the city may not actually publish the sex work incidents.

	- If there are incidents labeled as "prostitution" in anyway, doublecheck that at least some of the incidents are from after 2000

	- Also make sure that there are "prost" incidents OTHER THAN "human trafficking" specific reports. After all, we aren't trying to help traffickers avoid arrest!

## Adding the Data From a New City
- Once you find an appropriate city's API, open up the seed.py file

### Finding the API URL Endpoint
- First, find the appropriate API URL endpoint. This varies from city to city and API to API.
	
	- The Socrata API uses modified NoSQL queries in it's URL endpoints. For most socrata databases, adding "?$where=pd_desc%20like%20%27%25PROST%25%27" to the URL will cover many dbases. You need to look at the field where "PROST" can be found. Sometimes its "pd_desc" or "incident_description" but you need to doublecheck and use that in the endpoint.

	- Also, by default, the Socrata API only provides a certain number of records (sometimes just 1000). If you find that you aren't getting all of the necessary records, add try adding "&$limit=50000" to the end of your URL to tell it to look for more than the default. This doesn't always work, but it does most of the time.

### Check the Location Type
- Ideally, each incident will have a lattitude and longitude associated with it which can then be added directly to the dBase (and then Google Maps can easily plot the point)

- If there is no lat/long and there is just an address associated with each incident, you need to geocode each incident before adding them to the dBase (it unfortunately takes to long for Google Maps to geocode points as the map renders, so the lat/long is necessary beforehang)

- If you find a quick/easy way to do this, PLEASE comment in the issue and add documentation.

- As of early July 2018, the best possibility is likely to save the datapoints to a separate file (probably a .csv). Then take that file (potentially broken down into smaller files if necessary) and use a third party site to batch georeference the data and save the lat/long info to each row in the file. Then, you can use that file (with the lat/long) info to add incidents to the dBase from the file, rather than directly from the API.

### Add the Police Department and API Source to the dBase
- Look at the fill_basics function

	- For your new API, first add a Police Department record to the Database. For Example:

		Police9 = Police(police_dept_id=9, name="New York Police Department", city="New York", state="NY")
		
		db.session.add(Police9)
		
		db.session.commit

		- Make sure you add a new unique police_dept_id number and then actually add and commit it to the session. Note that a single city may actually have multiple law enforcement agencies publishing in multiple API's, which is why the police dept is separated from the source record.

	- Then add a Source Record (referencing the appropriate police_dept_id number) to the dbase. For example:

		source11 = Source(source_id=11, s_name="socrata", police_dept_id=9, s_description="NYPD Socrata API Historic Data", url="https://data.cityofnewyork.us/resource/9s4h-37hy.json?$where=pd_desc%20like%20%27%25PROST%25%27&$limit=50000", s_type="gov api")
		
		db.session.add(source11)
		
		db.session.commit

### Actually Adding the Incident Data
- Look at the table for Incidents in the model.py file to see the fields applicable...Most, like the city and datetime are pretty self-explanatory. Make sure you find the police report ID (THEIR unique field for each incident) so you can add that to the police_rec_num field for the incident.

- Look at the function "add_incident_data" and use it as a template for seeding the new city. You can either make a standalone function or add it as another "elif" to the add_incident_data_start function. Eventually, this should be all be uniform, but formatting the seed file is a relatively low priority.