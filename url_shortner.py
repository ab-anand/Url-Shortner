import requests
import sqlite3
import config
from urllib.parse import urlparse
from flask import Flask, g, request,redirect, url_for
from flask import render_template, abort
from base62 import toBase62, toBase10


app = Flask(__name__)


def connect_db():
	return sqlite3.connect(config.DATABASE_NAME)


@app.before_request
def before_request():
	g.db = connect_db()


@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == 'GET':
		return render_template('index.html')

	elif request.method == 'POST':

		original_url = request.form.get('url')
		if urlparse(original_url).scheme == '':
			original_url = 'http://' + original_url

		try:
			cursor = g.db.execute('''
						SELECT id FROM urls WHERE original_url = ? LIMIT 1
						''', (original_url,))
			encoded_value = toBase62(cursor.fetchone()[0])
		except TypeError as e:	
			cursor = g.db.execute('''
					INSERT OR IGNORE INTO urls (original_url)
			VALUES (?)''', (original_url,))	
			g.db.commit()
			encoded_value = toBase62(cursor.lastrowid)

		kwargs = {
			'result_url': 'http://' + request.host + '/' + encoded_value,
			'original_url': original_url
		}

		return render_template('index.html', **kwargs)


@app.route('/<url_short>')
def shortened(url_short):
	if str(url_short) != 'favicon.ico':
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


@app.route('/stats')
def get_stats():
	cursor = g.db.execute('''
				SELECT id, original_url, visited FROM urls 
				ORDER BY visited DESC LIMIT 5
		''')

	g.db.commit()
	elements = cursor.fetchall()

	return render_template('stats.html', elements=elements)


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404


if __name__ == "__main__":
	app.debug = True
	host = '0.0.0.0'
	port = 8000
	app.run(host, port)