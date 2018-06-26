# The SafeWork Project

The SafeWork Project is a sex worker support web app designed to help provide sex workers resources in an increasingly difficult and dangerous environment.

## Getting Started
(Runs on Ubuntu/Linux running at least Python 2.7)

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

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
