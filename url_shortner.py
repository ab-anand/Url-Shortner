import requests
import sqlite3
import config
from urllib.parse import urlparse
from flask import Flask, g, request,redirect, url_for
from flask import render_template, abort
from base62 import toBase62, toBase10


app = Flask(__name__)


def connect_db():
	'''this function opens 
	a connection with the database 
	mentioned in cofig.py file
	'''
	return sqlite3.connect(config.DATABASE_NAME)


@app.before_request
def before_request():
	'''this before_request decorator allows
	us to create a function that will run
	before each request. in this case we would
	connect with the database before each request	
	'''
	g.db = connect_db()


@app.route('/', methods=['POST', 'GET'])
def home():
	'''this route handles the homepage,
	run the normal if it is a GET request,
	if it is a POST request then performs the 
	required queries to hand over the data
	'''

	if request.method == 'GET':
		return render_template('index.html')

	elif request.method == 'POST':

		# get the original url from the form
		original_url = request.form.get('url')

		# if the url does not starts with http or https
		if urlparse(original_url).scheme == '':
			original_url = 'http://' + original_url


		# check if the url is already present in the database
		try:
			cursor = g.db.execute('''
						SELECT id FROM urls WHERE original_url = ? LIMIT 1
						''', (original_url,))
			encoded_value = toBase62(cursor.fetchone()[0])

		# if it is not present then push it in the DB
		except TypeError as e:	
			cursor = g.db.execute('''
					INSERT OR IGNORE INTO urls (original_url)
			VALUES (?)''', (original_url,))	
			g.db.commit()
			encoded_value = toBase62(cursor.lastrowid)

		# the values to be returned 
		kwargs = {
			'result_url': 'http://' + request.host + '/' + encoded_value,
			'original_url': original_url
		}

		return render_template('index.html', **kwargs)


@app.route('/<url_short>')
def shortened(url_short):
	'''redirects to the original page 
	using the shorten link provided.
	Return 404 if the link isn't in the DB
	'''

	try:
		decoded_url = toBase10(url_short)
		cursor = g.db.execute('''
					UPDATE urls SET visited = visited + 1 
					WHERE id=?''', (decoded_url,))
		cursor = g.db.execute('''
					SELECT original_url FROM urls 
					WHERE id=?''', (decoded_url,))
		g.db.commit()

		try:
			redirect_to_url = cursor.fetchone()[0]
		except TypeError as e:
			return abort(404)
		
		return redirect(redirect_to_url)

	# when the page is loaded the there is a request for 
	# "http://localhost:8000/favicon.ico" which causes the 
	# sqlite integer overflow because it converts "favicon.ico"
	# to base10 which become larger than the sqlite MAX Integer range.
	
	except OverflowError as e:
		print(str(e))


@app.route('/stats')
def get_stats():
	'''sends the top 5 visited urls 
	from the DB 
	'''
	cursor = g.db.execute('''
				SELECT id, original_url, visited FROM urls 
				ORDER BY visited DESC LIMIT 5
		''')

	g.db.commit()
	elements = cursor.fetchall()

	return render_template('stats.html', elements=elements)


@app.errorhandler(404)
def not_found(error):
	'''handles the 404 error
	'''
	return render_template('404.html'), 404

# run the app
if __name__ == "__main__":

	app.debug = True
	host = '0.0.0.0'
	port = 8000
	app.run(host, port)