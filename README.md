Cookiecutter-Behave-Selenium
============================

Is a [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.3/) template for BDD tests using Behave and Selenium. 
This repository was inspired by another two:
[cookiecutter-behave](https://github.com/dunossauro/cookiecutter-behave) and 
[BDD Automation Framework](https://github.com/pradeepta02/python-behave-automation-framework). 
I wanted the idea of a cookiecutter template, as the first 
mentioned, but with the complexity of the second. Then I mixed both with some adjustments and here it is :)

Requirements
------------
Install `cookiecutter` command line:
```
pip install cookiecutter
```

Usage
-----
You can generate your template by running:
```
cookiecutter gh:marcelolleivas/template-behave-selenium
```

Structure
----------
```
.
├── example
│   ├── features
│   │   ├── environment.py
│   │   ├── feature_name.feature
│   │   └── steps
│   │       └── step_name.py
│   ├── support
│   │   ├── __init__.py
│   │   ├── assistant.py
│   │   ├── driver_factory.py
│   │   ├── core
│   │   │   ├── element_action.py
│   │   │   └── __init__.py
│   │   ├── locators
│   │   │   ├── base_page.py
│   │   │   └── __init__.py   
│   │   └── page_actions
│   │       └── __init__.py
│   └── utils
│       ├── __init__.py
│       ├── assert_utils.py
│       ├── constant.py
│       └── logging.json
├── .gitignore
├── README.md
├── behave.ini
├── docker-compose.yml
└── pyproject.toml
```
