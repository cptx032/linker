# coding: utf-8
# Author: Willie Lawrence - cptx032 arroba gmail dot com

from bottle import (
    route, run, error, template,
    static_file, request, get, post, redirect,
    default_app, response)
from models import User, Elem, FOLDER, LINK

IS_IN_PYTHONANYWHERE = False


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


@get('/api/v1/link/<id:int>/')
def get_folder_childs(id):
    root = Elem.get_by_id(id)
    if not root:
        return {'error': u'not found'}
    links = root.get_elems()

    tree = []
    elem_i = root
    while elem_i is not None:
        tree.insert(0, elem_i)
        elem_i = elem_i.get_parent()

    return {
        'folder': root.__dict__,
        'childs': [i.__dict__ for i in links],
        'tree': [i.__dict__ for i in tree]
    }


@route('/images/<filename>')
@auth
def server_static(filename):
    return static_file(filename, root='static')


@get('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')


@get('/add/<parent_id:int>/<edit_id:int>')
@auth
def get_add(parent_id, edit_id):
    edit_object = Elem.get_by_id(edit_id)
    return template('add', parent_id=parent_id, edit_object=edit_object)


@post('/add')
@auth
def post_add():
    edit_id = int(request.forms.edit_id)
    parent = int(request.forms.parent_id)
    name = request.forms.name
    description = request.forms.description
    if (name.strip() == '') or (description.strip() == ''):
        return 'title or description cannot be empty'

    already_registered = Elem.search_by_name_description(name, description)
    if already_registered:
        return 'link/folder already registered'

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
        return redirect('/view/%d' % (parent.id))


@error(404)
@auth
def error404(error):
    return 'Nothing here, sorry'


def get_permissions():
    user = User.get_user_by_name(request.get_cookie('user'))
    if not user:
        return {
            'can_add': False,
            'can_see': False,
            'can_edit': False,
            'can_delete': False,
            'username': request.get_cookie('user')
        }
    return {
        'can_add': 'a' in user.authstring,
        'can_see': 's' in user.authstring,
        'can_edit': 'e' in user.authstring,
        'can_delete': 'd' in user.authstring,
        'username': request.get_cookie('user')
    }


@route('/view/<id:int>')
@auth
def view_folder(id):
    root = Elem.get_by_id(id)
    if not root:
        return 'not found'

    # getting all childrens (links/folders)
    links = root.get_elems()
    # the order if date asc, so go desc
    links.reverse()

    # getting the parent tree
    tree = []
    elem_i = root
    while elem_i is not None:
        tree.insert(0, elem_i)
        elem_i = elem_i.get_parent()

    return template(
        'view',
        folder_id=root.id,
        folder_parent=root.parent,
        elems=links,
        parent_tree=tree,
        **get_permissions()
    )


@get('/search/<term>')
@auth
def search_get(term):
    return template('search')

if IS_IN_PYTHONANYWHERE:
    application = default_app()
else:
    run(host='localhost', port=8081, debug=True)
