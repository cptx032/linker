# coding: utf-8
import sys
import sqlite3
from bottle import route, run, error, template, static_file, request, get, post

connection = sqlite3.connect('db.db')
cursor = connection.cursor()

ELEM_TABLE = '''
CREATE TABLE ELEM (
	ID INTEGER PRIMARY KEY,
	NAME TEXT NOT NULL,
	TYPE INTEGER NOT NULL,
	DESCRIPTION TEXT NOT NULL,
	PARENT INTEGER
)
'''

if len(sys.argv) > 1:
	if sys.argv[1] == 'create-db':
		cursor.execute(ELEM_TABLE)
		connection.commit()
		connection.close()
		sys.exit(0)

FOLDER = 1
LINK = 2

class Elem:
	def __init__(self, id, type, name, desc):
		assert(type in [FOLDER, LINK])
		self.id = id
		self.type = type
		self.name = name
		self.desc = desc

@route('/')
def hello():
	return 'fixme'

@route('/images/<filename>')
def server_static(filename):
	return static_file(filename, root='./static')

@get('/add/<parent_id:int>')
def get_add(parent_id):
	return template('add', parent_id=parent_id)

@error(404)
def error404(error):
	return 'Nothing here, sorry'

@route('/view/<id:int>')
def view_folder(id):
	folder_1 = Elem(1, FOLDER, 'Tools', 'A set of general tools')
	link_1 = Elem(2, LINK, 'DuckduckGo', 'http://duckduckgo.com')
	return template(
		'view',
		folder_name='Root',
		folder_id=0,
		elems=[folder_1, link_1]
	)
	
run(host='localhost', port=8080, debug=True)
connection.close()