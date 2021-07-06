# {{cookiecutter.project_name}} #

{{cookiecutter.project_short_description}}

Usage
-----
For execute this repo you must have to get [Poetry](https://python-poetry.org/) installed.

After installed it, activate your virtual environment using the following command
```
poetry shell
```
Then install the dependencies:
```
poetry install
```

How to run
----------

#### Webdriver Manager ####

If you want to run the tests using [Webdriver Manager](https://pypi.org/project/webdriver-manager/) 
please set the variables on ```behave.ini```:

* Set ```application_url``` with the url you will test;
* Set ```browser``` as ```chrome``` or ```firefox```;
* Set the ```element_fetch_timeout``` time as convenient;
* Set the ```implicit_timeout``` time as convenient;
* Set ```use_grid```, on ```behave.ini``` as ```False```;

With the settings done you can run the tests:
```
behave features/
```

Or testing single features:
```
behave features/{feature_name}
```

#### Selenium Grid ####

If you want to run the tests using [Selenium Grid](https://www.selenium.dev/documentation/en/grid/) 
please set the variables on ```behave.ini```:

* Set ```application_url``` with the url you will test;
* Set ```browser``` as ```chrome``` or ```firefox```;
* Set the ```element_fetch_timeout``` time as convenient;
* Set the ```implicit_timeout``` time as convenient;
* Set ```use_grid```, on ```behave.ini``` as ```True```;

Beyond these settings, you must have [Docker Compose](https://docs.docker.com/compose/install/) installed.

With all that done, you must have to get your ```docker-compose.yml``` up:
```
docker-compose up
```

Then, to test all the features:

```
behave features/
```

Or testing single features:
```
behave features/{feature_name}
```

Results
-------
After the tests are finished, it creates a folder ```log``` where you can get more details about all that was run. 




