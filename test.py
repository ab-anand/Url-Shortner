import sqlite3

cn = sqlite3.connect('urls.db')
conn = cn.cursor()

# a = conn.execute('''
# 	SELECT * FROM urls
# 	''')
# original_url = 'http://zetcode.com/db/sqlitepythontutorial/'
# url2 = 'https://github.com/narenaryan?tab=repositories'
# q = conn.execute('''
# 				INSERT OR IGNORE INTO urls (original_url)
# 		VALUES (?)''', (url2,))	
# cn.commit()
# print(q.lastrowid)
# p = conn.execute('''
# 				INSERT OR IGNORE INTO urls (original_url)
# 		VALUES (?)''', (url2,))	
# cn.commit()
a = conn.execute('''
	SELECT id, original_url, visited FROM urls 
				ORDER BY visited DESC LIMIT 10
	''')
print(a.fetchall())
# print(p.lastrowid)
# for x in a:
# 	print(x)