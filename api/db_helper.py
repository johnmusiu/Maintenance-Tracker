""" this module contains DB helper methods for db query methods"""
from flask import json
from .db_connect import DBConnect


def execute_query(query, values):
    """ runs all queries """
    try:
        db = DBConnect()
        db.connect().execute(query, values)
        db.conn.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def json_fetch_all(query, values):
    """ retrieve db data in json"""
    try:
        db = DBConnect()
        db.connect().execute(query, values)
        res = json.dumps(db.cursor.fetchall(), indent=2)
        db.close_conn()
        return res
    except Exception as ex:
        print(ex)
        return False


def json_fetch_one(query, values):
    """ retrieve one db data result in json"""
    try:
        db = DBConnect()
        db.connect().execute(query, values)
        res = json.dumps(db.cursor.fetchone())
        db.close_conn()
        return res
    except Exception as ex:
        print(ex)
        return False


def fetch_one(query, values):
    """ retrieve one db data result"""
    try:
        db = DBConnect()
        db.connect().execute(query, values)
        res = db.cursor.fetchone()
        db.close_conn()
        return res
    except Exception as ex:
        print(ex)
        return False


def fetch_all(query):
    """ retrieve one db data result"""
    try:
        db = DBConnect()
        db.connect().execute(query)
        res = db.cursor.fetchall()
        db.close_conn()
        return res
    except Exception as ex:
        print(ex)
        return False
