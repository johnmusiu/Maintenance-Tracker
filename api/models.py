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
        # check if email taken
        sql = "SELECT * FROM users where email = %s;"
        values = (email,)
        user = fetch_one(sql, values)
        if not user:
            password = generate_password_hash(password)
            sql = u"INSERT INTO users(first_name, last_name,\
                            email, password, is_admin) \
                            VALUES(%s, %s, %s, %s, '0');"

            values = (fname, lname, email, password,)
            execute_query(sql, values)
            result = (True, email, fname, lname)
        else:
            result = (
                False,
                "Email address already registered under another account")
        return result

    def signin(self, email, password):
        """ function to verify user details on login """
        sql = u"SELECT * FROM users where email = %s;"
        values = (email,)
        user = fetch_one(sql, values)
        if user is None:
            return False
        else:
            if check_password_hash(user[4], password):
                result = ({'id': user[0], 'is_admin': user[7]})
            else:
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

class Admin(User):
    """ admin user class """
    def __init__(self):
        """ inherit user methods """
        User.__init__(self)
    
    def approve(self, request_id):
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

    def disapprove(self, request_id):
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

    def resolve(self, request_id):
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

    def get_all_requests(self):
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

    def get_request_by_id(self, request_id):
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
    
class NormalUser(User):
    """ normal user class ie. has no admin priviledges """
    def __init__(self):
        User.__init__(self)
    
    def make_request(self, title, description, category):
        """ user create request """
        request = Request(title, description, category)
        return request.create()

    def update_request(self, request_id, title, description, category):
        """ user update request """
        request = Request(title, description, category, request_id)
        return request.update()
        
    def get_requests(self):
        """ get user requests """
        return Request().get_user_requests()

    def get_request_by_id(self, request_id):
        """ get user request by id """
        return Request().get_by_id(request_id)
        
class Request():
    """ the requests model """

    def __init__(self, title=None, description=None, category=None, request_id=None):
        """initialize instance variables """
        self.title = title
        self.description = description
        self.category = category
        self.request_id = request_id

    def create(self):
        """ save request """
        # check if a similar open or pending request exists for the user
        db = DBConnect()
        cursor = db.connect()
        # check if email taken
        try:
            sql = u"SELECT * FROM requests where user_id = %s and \
                            title = %s and (status = 'pending' \
                            or status = 'open') and type = %s;"
            values = (session['user_id'], self.title, self.category,)
            requests = fetch_one(sql, values)

            if requests:
                result = (False,
                          "Request already exists, wait for resolution!")
            else:
                cursor.execute(u"INSERT INTO requests(user_id, type, title,\
                            description, created_at, updated_at, status)\
                           VALUES(%s, %s, %s, %s, current_timestamp, \
                           current_timestamp, 'open') \
                           RETURNING request_id;",
                               (session['user_id'], self.category, self.title, 
                               self.description,))
                db.conn.commit()
                res_id = cursor.fetchone()[0]
                result = (True, res_id)
        except Exception:
            result = (False)
        return result

    def get_user_requests(self):
        """ get my requests """
        sql = "SELECT * FROM requests where user_id = %s;"
        values = (session['user_id'],)
        requests = fetch_all(sql, values)

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
        return result

    def update(self):
        """ update request """
        # check if request exists
        sql = u"SELECT * FROM requests where request_id = %s;"
        values = (self.request_id,)
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
                values = (self.title, self.description, self.category, 
                            self.request_id,)
                res = execute_query(sql, values)
                result = (True, values)
        return result

    def get_by_id(self, request_id):
        """ get user request by id"""
        sql = u"SELECT * FROM requests WHERE request_id = %s AND user_id = %s;"
        values = (request_id, session['user_id'],)
        request = fetch_one(sql, values)
        if not request:
            return (False, "Request id not found.", 404)
        result = {
            "title": request[5],
            "description": request[6],
            "type": request[4],
            "status": request[3],
            "resolved_at": request[9],
            "created_at": request[7]
        }
        return (True, result)
