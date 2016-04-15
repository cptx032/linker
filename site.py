# coding: utf-8
# Author: Willie Lawrence - cptx032 arroba gmail dot com
import sys
import sqlite3
from bottle import route, run, error, template, static_file, request, get, post, redirect, default_app, response

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

USER_TABLE = '''
CREATE TABLE USER (
	ID INTEGER PRIMARY KEY,
	NAME TEXT NOT NULL,
	AUTHSTRING TEXT
)
'''

class User:
	def __init__(self, id, name, authstring):
		self.id = id
		self.name = name
		self.authstring = authstring
	
	@staticmethod
	def get_user_by_name(name):
		sql = '''SELECT * FROM USER WHERE NAME=?'''
		cursor.execute(sql, (name,))
		row = cursor.fetchone()
		if not row:
			return None
		return User(*row)
	
	@staticmethod
	def insert(elem):
		sql = '''INSERT INTO USER (NAME, AUTHSTRING)
		VALUES (?,?)
		'''
		cursor.executemany(sql, [(elem.name, elem.authstring)])
	
	def update(self):
		sql = '''UPDATE USER SET NAME=?, AUTHSTRING=? WHERE ID=?'''
		cursor.execute(sql, (self.name, self.authstring, self.id))

	def remove(self):
		childs = self.get_elems()
		for i in childs:
			i.remove()
		# removing it self
		sql = '''DELETE FROM USER WHERE ID=?'''
		cursor.execute(sql, (self.id,))

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

	def update(self):
		sql = '''UPDATE ELEM SET NAME=?, TYPE=?, DESCRIPTION=? WHERE ID=?'''
		cursor.execute(sql, (self.name, self.type, self.desc, self.id))
	
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
	cursor.execute(USER_TABLE)
	User.insert(User(None, 'sky', 'sade')) # see, add, delete, edit
	User.insert(User(None, 'guest', 's'))
	Elem.insert(Elem(None, 'Root', FOLDER, 'root', None))
	connection.commit()
	connection.close()

if len(sys.argv) > 1:
	if sys.argv[1] == 'create-db':
		initial_config()
		sys.exit(0)

@route('/auth')
def set_user():
	return template('auth')

@post('/auth')
def post_auth():
	username = request.forms.get('name')
	if username:
		response.set_cookie('user', username)
	return redirect('/')

def auth(func):
	def r(*args, **kws):
		return redirect('/auth')

	def ver(*args, **kws):
		if request.get_cookie('user'):
			return func(*args, **kws)
		else:
			return r()
	return ver

@route('/logout')
def logout():
	response.delete_cookie('user')
	return redirect('/')

@route('/')
@auth
def index():
	return redirect('/view/1')

@route('/images/<filename>')
@auth
def server_static(filename):
	return static_file(filename, root='static')

@get('/add/<parent_id:int>/<edit_id:int>')
@auth
def get_add(parent_id, edit_id):
	edit_object = Elem.get_by_id(edit_id)
	return template('add', parent_id=parent_id, edit_object=edit_object)

@post('/add')
@auth
def post_add():
	edit_id = int(request.forms.get('edit_id'))
	parent = int(request.forms.get('parent_id'))
	name = request.forms.get('name')
	description = request.forms.get('description')
	type = FOLDER
	if description.lower().startswith('http'):
		type = LINK
	if edit_id > 0:
		elem = Elem.get_by_id(edit_id)
		elem.name = name
		elem.desc = description
		elem.type = type
		elem.update()
	else:
		Elem.insert(
			Elem(None, name, type, description, parent)
		)
	connection.commit()
	return redirect('/view/%d' % (parent))

@route('/delete/<id:int>')
@auth
def delete_get(id):
	elem = Elem.get_by_id(id)
	parent = elem.get_parent()
	if not elem:
		return 'not found'
	else:
		elem.remove()
		connection.commit()
		return redirect('/view/%d' % (parent.id))

@error(404)
@auth
def error404(error):
	return 'Nothing here, sorry'

def get_permissions():
	user = User.get_user_by_name(request.get_cookie('user'))
	if not user:
		return {
			'can_add'    : False,
			'can_see'    : False,
			'can_edit'   : False,
			'can_delete' : False,
			'username'   : request.get_cookie('user')
		}
	return {
		'can_add'    : 'a' in user.authstring,
		'can_see'    : 's' in user.authstring,
		'can_edit'   : 'e' in user.authstring,
		'can_delete' : 'd' in user.authstring,
		'username'   : request.get_cookie('user')
	}

@route('/view/<id:int>')
@auth
def view_folder(id):
	root = Elem.get_by_id(id)
	if not root:
		return 'not found'
	
	return template(
		'view',
		folder_name=root.name,
		folder_id=root.id,
		folder_parent=root.parent,
		elems=root.get_elems(),
		**get_permissions()
	)

if IS_IN_PYTHONANYWHERE:
	application = default_app()
else:
	run(host='localhost', port=8080, debug=True)
	connection.close()