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
```
    Url-Shortner/
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
    ├──  SETUP.md
    ├──  requirements.txt
    ├──  schema.sql           # schema for the DB
    ├──  urls.db              # the DB
    └──  test.py 	          # some tests on the DB
```

## Setup

Visit the [Setup file](SETUP.md)

## Architecture

* The framework selected for the operation is Flask because of the ease of its setup readability of the code.
* The Database selected is SQLite, although there is no relationship to maintain among
the tables and thus going with NoSql DB would have worked too.
* The schema has been kept minimal to avoid extra space usage as well as maintaining low latency. Shown below
```	
	database/
	└── urls(table)
		├── id
		├── original_url
		└── visited

```
* In the DB the `visited` column helps in click tracking. It maintains the number of times the shortened link has been open.
* For any given URL:
	* We insert the record in the DB.
	* Convert the returned record ID to base62 string
	* Return the final shotened url to the user.

* When a user visits the short url:
	* We convert the string to base10.
	* Check if any record is present with that id
	* Redirect to that original url if present
	* otherwise return 404
	* While converting to base10 we also put a check to avoid Integer Overflow Error.

* Some important features of the system:
	* Query params are not ignored.
	* No restriction over the url length.


## Scalability

* The base62 algorithm provides 62 options for each digits.
* In our case, there is no restriction over the shortened url created.
* Example, if the shortened url is restricted to be of length 6
```
	Options for each character = 62
	Total unique string possible => 62^8 = ~ 2.1834011e+14
```