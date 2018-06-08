"""
    defines the data models of the app
"""
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import session
from .db_helper import execute_query, fetch_one, fetch_all
from .db_connect import DBConnect


class User():
    """ the user model methods"""

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = str(password)

    def signup(self, fname, lname, email, password):
        """ define method to create an account"""
        try:
            db = DBConnect()
            cursor = db.connect()
            # check if email taken
            cursor.execute("SELECT * FROM users where email = %s;", (email,))
            user = cursor.fetchone()
            if not user:
                password = generate_password_hash(password)
                cursor.execute(u"INSERT INTO users(first_name, last_name,\
                            email, password, is_admin) \
                            VALUES(%s, %s, %s, %s, '0');",
                               (fname, lname, email, password))
                db.conn.commit()
                result = (True, email, fname, lname)
            else:
                result = (
                    False,
                    "Email address already registered under another account")
        except Exception as ex:
            print(ex)
            result = (False, "Internal error, contact admin")
        return result

    def signin(self, email, password):
        """ function to verify user details on login """
        try:
            db = DBConnect()
            cursor = db.connect()
            cursor.execute("SELECT * FROM users where email = %s;", (email,))
            user = cursor.fetchone()
            if user is None:
                return False
            else:
                if check_password_hash(user[4], password):
                    result = ({'id': user[0], 'is_admin': user[7]})
                else:
                    result = False
        except Exception as ex:
            print(ex)
            result = False
        return result

    def generate_token(self, email, is_admin, user_id):
        """
            Generates the Auth Token for the currently logging in user
            :returns: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': email,
                'user_id': user_id,
                'role': is_admin
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e


class Request():
    """ the requests model """

    def __init__(self):
        """initialize instance variables """

    def save(self, user_id, category, title, description):
        """ save request """
        # check if a similar open or pending request exists for the user
        """ get my requests """
        db = DBConnect()
        cursor = db.connect()
        # check if email taken
        try:
            cursor.execute(u"SELECT * FROM requests where user_id = %s and \
                            title = %s and (status = 'pending' \
                            or status = 'open') and type = %s;",
                           (user_id, title, category,))
            requests = cursor.fetchone()

            if requests:
                result = (False,
                          "Request already exists, wait for resolution!")
            else:
                cursor.execute(u"INSERT INTO requests(user_id, type, title,\
                            description, created_at, updated_at, status)\
                           VALUES(%s, %s, %s, %s, current_timestamp, \
                           current_timestamp, 'open') \
                           RETURNING (request_id, title);",
                               (user_id, category, title, description,))
                db.conn.commit()
                res = cursor.fetchone()[0]
                result = (True, res)
        except Exception:
            result = (False)
        return result

    def get_all_my_requests(self, user_id):
        """ get my requests """
        db = DBConnect()
        cursor = db.connect()
        # check if email taken
        try:
            cursor.execute("SELECT * FROM requests where user_id = %s;",
                           (user_id,))
            requests = cursor.fetchall()

            if not requests:
                result = False
            else:
                result = {}
                for request in requests:
                    result[request[0]] = {
                        "title": request[5],
                        "description": request[6],
                        "type": request[4],
                        "status": request[3],
                        "resolved_at": request[9],
                        "created_at": request[7]
                    }
        except Exception as e:
            print(e)
            result = False
        db.close_conn()
        return result

    def update(self, user_id, request_id, title, description, category):
        """ update request """
        try:
            # check if request exists
            sql = u"SELECT * FROM requests where request_id = %s;"
            values = (request_id,)
            res = fetch_one(sql, values)
            if not res:
                result = (False, "This request does not exist!", 404)
            else:
                if res[1] != session['user_id']:
                    result = (
                        False, "You can only update your own requests", 401)
                elif res[3] != 'open':
                    result = (
                        False, "Editing this request is not allowed", 403)
                else:
                    sql = u"UPDATE requests SET title=%s, description=%s,\
                            type=%s, updated_at=current_timestamp \
                            WHERE request_id=%s;"
                    values = (title, description, category, request_id,)
                    res = execute_query(sql, values)
                    result = (True, values)
        except Exception as ex:
            print(ex)
        return result

    def get_by_id(self, request_id):
        """ get request by id"""
        sql = u"SELECT * FROM requests WHERE request_id = %s AND user_id = %s;"
        values = (request_id, session['user_id'],)
        request = fetch_one(sql, values)
        if not request:
            return (False, "This request does not exist!", 404)
        result = {
            "title": request[5],
            "description": request[6],
            "type": request[4],
            "status": request[3],
            "resolved_at": request[9],
            "created_at": request[7]
        }
        return (True, result)

    @staticmethod
    def admin_get_all():
        """ get request by id"""
        sql = u"SELECT * FROM requests;"
        requests = fetch_all(sql)
        if not requests:
            return (False, "This request does not exist!", 404)
        result = {}
        for request in requests:
            result[request[0]] = {
                "title": request[5],
                "description": request[6],
                "type": request[4],
                "status": request[3],
                "resolved_at": request[9],
                "created_at": request[7]
            }
        return (True, result)

    @staticmethod
    def admin_get_by_id(request_id):
        """ get request by id"""
        sql = u"SELECT * FROM requests WHERE request_id = %s;"
        values = (request_id,)
        request = fetch_one(sql, values)
        if not request:
            return (False, "This request does not exist!", 404)
        result = {
            "title": request[5],
            "description": request[6],
            "type": request[4],
            "status": request[3],
            "resolved_at": request[9],
            "created_at": request[7]
        }
        return (True, result)

    @staticmethod
    def admin_approve(request_id):
        """ admin approve request"""
        sql = u"UPDATE requests SET status='pending' WHERE request_id = %s \
                RETURNING ('request_id');"
        values = (request_id,)
        request = execute_query(sql, values)
        if not request:
            return (False, "This request does not exist!", 404)
        result = {
            "message": "Request approved successfully",
            "request_id": request
        }
        return (True, result)

    @staticmethod
    def admin_disapprove(request_id):
        """ admin disapprove request """
        sql = u"UPDATE requests SET status='disapproved' WHERE request_id = %s \
                RETURNING ('request_id');"
        values = (request_id,)
        request = execute_query(sql, values)
        if not request:
            return (False, "This request does not exist!", 404)
        result = {
            "message": "Request disapproved successfully",
            "request_id": request
        }
        return (True, result)

    @staticmethod
    def admin_resolve(request_id):
        """ admin resolve request"""
        sql = u"UPDATE requests SET status='resolved' WHERE request_id = %s \
                RETURNING ('request_id');"
        values = (request_id,)
        request = execute_query(sql, values)
        if not request:
            return (False, "This request does not exist!", 404)
        result = {
            "message": "Request resolved successfully",
            "request_id": request
        }
        return (True, result)
