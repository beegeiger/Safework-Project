# The SafeWork Project

The SafeWork Project is a sex worker support web app designed to help provide sex workers resources in an increasingly difficult and dangerous environment.

Currently located at safeworkproject.org

## Getting Started

### Prerequisites

-Running a Linux System (Developed and Tested on Ubuntu 16.04)

-System can run Python 2.7+

### Installing

-Clone/Download the repo from https://github.com/beegeiger/Safework-Project

-Create a virtual environment ($virtualenv env) and activate it ($source env/bin/activate)

-Install requirements ($pip install -r requirements.txt)

-Create psql database called "safework" ($createdb safework)
-Seed Database:

	-Make sure the entire line in server.py that begins with "from model import..." is commented out

	-Make sure that the line in model.py "from server import app" is NOT commented out

	-Run model.py ($python model.py)

	-In seed.py, make sure the function calls are not commented out (and as of 6/25/18, the "add_incident_data" function call should be "add_incident_data([3, 4, 5, 6, 7, 8, 9, 10, 11])")

	-Run seed.py (python seed.py)

	-Comment back out the line in model.py "from server import app"

	-Uncomment the entire line in server.py that begins with "from model import..."

-Run server.py ($python server.py)

-The app should be running on your local system!


## Testing

Tests for the SafeWork Project can be found in tests.py. Right now, only a relatively small portion of the app is tested and adding tests is a top priority!

## Deployment

The app is currently live at safeworkproject.org and is running on an AWS lightsail server using nginx as a proxy server to only make connections through https.

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/beegeiger/Safework-Project/tags). 

## Authors

* **Dorothy Bee Geiger** - *Initial work* - [SafeWork Project](https://github.com/beegeiger/Safework-Project)

See also the list of [contributors](https://github.com/beegeiger/Safework-Project/contributors) who participated in this project.

## Acknowledgments

* Hackbright Academy for Teaching Dorothy Bee the Basics to create this app.
