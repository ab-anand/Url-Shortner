## URL Shortner 
![Python 3x](https://img.shields.io/pypi/pyversions/django?color=green&style=plastic)

---

This project is aimed to create a URL Shorter which would take the long urls and convert it to condensed form 
maintaining all the useful information it contains such as `query params`.

---

## Environment

* python3
* flask
* Linux Mint


## Project Structure

    Url-Shortner
    ├── bin
    │	├── setup
    │   └── setup.sh 	   # setting up the project
    ├── templates          # all the html templates         
    │   ├── index.html          
    │   ├── base.html         
    │   ├── stats.html 
    │	└── 404.html          
    ├──  url_shortner.py      # handle all the routes
    ├──  base62.py            # converts base10 to base62 and vice-versa
    ├──  config.py            # database configuration
    ├──  README.md
    ├──  requirements.txt
    ├──  schema.sql           # schema for the DB
    ├──  urls.db              # the DB
    └──  test.py 	          # some tests on the DB


## Setup

Visit the [Setup file](setup.md)