# coding: utf-8
# Author: Willie Lawrence - cptx032 arroba gmail dot com
import sys
import sqlite3
from bottle import route, run, error, template, static_file, request, get, post, redirect

connection = sqlite3.connect('./db.db')
cursor = connection.cursor()

IS_IN_PYTHONANYWHERE = False

ELEM_TABLE = '''
CREATE TABLE ELEM (
	ID INTEGER PRIMARY KEY,
	NAME TEXT NOT NULL,
	TYPE INTEGER NOT NULL,
	DESCRIPTION TEXT NOT NULL,
	PARENT INTEGER
)
'''

FOLDER = 1
LINK = 2

class Elem:
	def __init__(self, id, name, type, desc, parent=None):
		assert(type in [FOLDER, LINK])
		self.id = id
		self.type = type
		self.name = name
		self.desc = desc
		self.parent = parent
	
	def get_parent(self):
		if self.parent:
			return Elem.get_by_id(self.parent)
		else:
			return self
	
	def get_elems(self):
		sql = '''SELECT * FROM ELEM WHERE PARENT=?'''
		return [Elem(*i) for i in cursor.execute(sql, (self.id,))]

	def remove(self):
		childs = self.get_elems()
		for i in childs:
			i.remove()
		# removing it self
		sql = '''DELETE FROM ELEM WHERE ID=?'''
		cursor.execute(sql, (self.id,))

	@staticmethod
	def insert(elem):
		sql = '''INSERT INTO ELEM (NAME, TYPE, DESCRIPTION, PARENT)
		VALUES (?,?,?,?)
		'''
		cursor.executemany(sql, [(elem.name, elem.type, elem.desc, elem.parent)])

	@staticmethod
	def get_by_id(id):
		sql = '''SELECT * FROM ELEM WHERE ID=?'''
		cursor.execute(sql, (id,))
		row = cursor.fetchone()
		if not row:
			return None
		return Elem(*row)

def initial_config():
	cursor.execute(ELEM_TABLE)
	Elem.insert(Elem(None, 'Root', FOLDER, 'root', None))
	connection.commit()
	connection.close()

if len(sys.argv) > 1:
	if sys.argv[1] == 'create-db':
		initial_config()
		sys.exit(0)

@route('/')
def hello():
	return 'fixme'

@route('/images/<filename>')
def server_static(filename):
	return static_file(filename, root='static')

@get('/add/<parent_id:int>')
def get_add(parent_id):
	return template('add', parent_id=parent_id)

@route('/add', method='POST')
def post_add():
	parent = int(request.forms.get('parent_id'))
	name = request.forms.get('name')
	description = request.forms.get('description')
	type = FOLDER
	if description.lower().startswith('http'):
		type = LINK
	Elem.insert(
		Elem(None, name, type, description, parent)
	)
	connection.commit()
	return redirect('/view/%d' % (parent))

@route('/delete/<id:int>')
def delete_get(id):
	elem = Elem.get_by_id(id)
	parent = elem.get_parent()
	if not elem:
		return 'not found'
	else:
		elem.remove()
		return redirect('/view/%d' % (parent.id))

@error(404)
def error404(error):
	return 'Nothing here, sorry'

@route('/view/<id:int>')
def view_folder(id):
	root = Elem.get_by_id(id)
	if not root:
		return 'not found'
	return template(
		'view',
		folder_name=root.name,
		folder_id=root.id,
		folder_parent=root.parent,
		elems=root.get_elems()
	)

if IS_IN_PYTHONANYWHERE:
	application = default_app()
else:
	run(host='localhost', port=8080, debug=True)
	connection.close()