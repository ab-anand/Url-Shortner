import sqlite3

cn = sqlite3.connect('urls.db')
conn = cn.cursor()

# check what data is present
z = conn.execute('''
	SELECT * FROM urls
	''')
print(z.fetchall())

# insert some data
original_url = 'http://zetcode.com/db/sqlitepythontutorial/'
url2 = 'https://github.com/narenaryan?tab=repositories'

# insert same data twice to check if new record is added
q = conn.execute('''
				INSERT OR IGNORE INTO urls (original_url)
		VALUES (?)''', (url2,))	
cn.commit()
print('inserted successfully')


p = conn.execute('''
				INSERT OR IGNORE INTO urls (original_url)
		VALUES (?)''', (url2,))	
cn.commit()
print('inserted successfully')

# fetch top visited links
a = conn.execute('''
	SELECT id, original_url, visited FROM urls 
				ORDER BY visited DESC LIMIT 10
	''')
print(a.fetchall())
# print(p.lastrowid)
# for x in a:
# 	print(x)