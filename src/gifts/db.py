import sqlite3 as s


def check_gift(id):
	with s.connect('src/gifts/db.db') as db:
		c = db.cursor()
		return c.execute('SELECT * FROM gifts WHERE id = ?', (id, )).fetchall()[0][1]		

#src/gifts/