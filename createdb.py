#!/usr/bin/env python
# coding: utf-8
# Author: Willie Lawrence - cptx032 arroba gmail dot com

import sqlite3
from models import User, Elem

ELEM_TABLE = '''
CREATE TABLE ELEM (
    ID INTEGER PRIMARY KEY,
    NAME TEXT NOT NULL,
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

try:
    Elem.get_by_id(1)
except sqlite3.OperationalError:
    print 'tables not found...creating tables'
    connection = sqlite3.connect('./db.db')
    cursor = connection.cursor()
    cursor.execute(ELEM_TABLE)
    cursor.execute(USER_TABLE)
    connection.commit()
    connection.close()

user_key = raw_input('Enter user key: ')
see = raw_input('It can see links? (y/n) ').lower() == 'y'
add = raw_input('It can add links? (y/n) ').lower() == 'y'
delete = raw_input('It can delete links?(y/n) ').lower() == 'y'
edit = raw_input('It can edit links? (y/n) ').lower() == 'y'

permission = ''
if see:
    permission += 's'
if add:
    permission += 'a'
if delete:
    permission += 'd'
if edit:
    permission += 'e'

User.insert(User(None, user_key, permission))

if not Elem.get_by_id(1):
    print 'No root element found...creating root folder'
    Elem.insert(Elem(None, 'Root', 'root', None))
