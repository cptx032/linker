# coding: utf-8
# Author: Willie Lawrence - cptx032 arroba gmail dot com
import sqlite3


class User:
    def __init__(self, id, name, authstring):
        self.id = id
        self.name = name
        self.authstring = authstring

    @staticmethod
    def get_user_by_name(name):
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()

        sql = '''SELECT * FROM USER WHERE NAME=?'''
        cursor.execute(sql, (name,))
        row = cursor.fetchone()

        connection.close()

        if not row:
            return None
        return User(*row)

    @staticmethod
    def get_all(name):
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()
        sql = '''SELECT * FROM USER'''
        cursor.execute(sql)
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return User(*row)

    @staticmethod
    def insert(elem):
        sql = '''INSERT INTO USER (NAME, AUTHSTRING)
        VALUES (?,?)
        '''
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()

        cursor.executemany(sql, [(elem.name, elem.authstring)])

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()

        sql = '''UPDATE USER SET NAME=?, AUTHSTRING=? WHERE ID=?'''
        cursor.execute(sql, (self.name, self.authstring, self.id))

        connection.commit()
        connection.close()

    def remove(self):
        childs = self.get_elems()
        for i in childs:
            i.remove()
        # removing it self
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()

        sql = '''DELETE FROM USER WHERE ID=?'''
        cursor.execute(sql, (self.id,))

        connection.commit()
        connection.close()

FOLDER = 1
LINK = 2


class Elem:
    def __init__(self, id, name, desc, parent=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.parent = parent

    def get_parent(self):
        if self.parent:
            return Elem.get_by_id(self.parent)
        else:
            return None

    def update(self):
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()

        sql = '''UPDATE ELEM SET NAME=?, DESCRIPTION=? WHERE ID=?'''
        cursor.execute(sql, (self.name, self.desc, self.id))

        connection.commit()
        connection.close()

    def get_elems(self):
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()
        sql = '''SELECT * FROM ELEM WHERE PARENT=?'''
        return [Elem(*i) for i in cursor.execute(sql, (self.id,))]
        connection.close()  # fixme

    def remove(self):
        childs = self.get_elems()
        for i in childs:
            i.remove()
        # removing it self
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()

        sql = '''DELETE FROM ELEM WHERE ID=?'''
        cursor.execute(sql, (self.id,))

        connection.commit()
        connection.close()

    @staticmethod
    def insert(elem):
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()
        sql = u'''INSERT INTO ELEM (NAME, DESCRIPTION, PARENT)
        VALUES (?,?,?)
        '''
        cursor.executemany(
            sql, [(elem.name, elem.desc, elem.parent)])

        connection.commit()
        connection.close()

    @staticmethod
    def get_by_id(id):
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()

        sql = '''SELECT * FROM ELEM WHERE ID=?'''
        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        connection.close()
        if not row:
            return None
        return Elem(*row)

    @staticmethod
    def search_by_name_description(name, description):
        connection = sqlite3.connect('./db.db')
        cursor = connection.cursor()

        sql = '''SELECT * FROM ELEM WHERE NAME=? AND DESCRIPTION=?'''
        cursor.execute(sql, (name, description))
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return Elem(*row)

    def __repr__(self):
        return u'({}) {} = {}'.format(
            self.id, self.name, self.desc)
