Cookiecutter-Behave-Selenium
============================

Template created for BDD tests using behave and selenium.

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

Estructure
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
