""" this module contains DB helper methods for db query methods"""
from .db_connect import DBConnect


def execute_query(query, values):
    """ runs all queries """
    try:
        db = DBConnect()
        db.connect().execute(query, values)
        db.conn.commit()
        return True
    except Exception:
        return False


def fetch_one(query, values):
    """ retrieve one db data result"""
    try:
        db = DBConnect()
        db.connect().execute(query, values)
        res = db.cursor.fetchone()
        db.close_conn()
        return res
    except Exception:
        return False


def fetch_all(query, values=""):
    """ retrieve one db data result"""
    try:
        db = DBConnect()
        db.connect().execute(query, values)
        res = db.cursor.fetchall()
        db.close_conn()
        return res
    except Exception:
        return False
