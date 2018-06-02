"""
    defines the data models of the app
"""
import os
from flask import current_app
import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

#initialize an empty requests list
requests = {}
users = {}

class User():
    """ the user model """

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        # self.password = generate_password_hash(password)
        self.password = password

    def signup(self):
        """ define method to create an account"""
        #check if email taken
        if users.get(self.email):
            return ("0", "Email address already registered under another account")
        count_users = len(users)
        users[self.email] = (count_users+1, self.name, self.password, self.email)
        return ("1", (count_users+1, self.email, self.name))

    def verify_password(self, password):
        """ function to verify password hash """
        print(check_password_hash(self.password, password))
        # return check_password_hash(self.password, password)
        if password == self.password:
            return True
        else:
            return False


    def generate_token(self, email):
        """
            Generates the Auth Token for the currently logging in user
            :returns: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': email
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_token(token):
        """
        Decodes the auth token on user request to the app
        """
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired'
        except jwt.InvalidTokenError:
            return 'Invalid'

        


                
class Request():
    """ the requests model """

    def __init__(self, title=None, description=None, category=None):
        """initialize instance variables """
        self.title = title
        self.description = description
        self.category = category
        self.status = "open"
        self.created_at = time.strftime('%A %B, %d %Y %H:%M:%S')
        self.updated_at = self.created_at
    
    def save(self, user_id):
        """ save request """
        #get my requests
        my_requests = requests.get(user_id, "0")
        count = 0
        for user, user_requests in my_requests.iteritems():
            count += len(user_requests)

        new_request = ({self.title: (count+1, self.description, self.category,
                                    user_id, self.status, self.created_at, 
                                    self.updated_at)})


        if my_requests != "0":
            """check if request already exists """
            is_exist = my_requests.get(self.title, "0")
            if is_exist == "0":
                requests[user_id].update(new_request)
                return ("1", new_request)
            else: 
                return ("0", "")
        else:
            requests[user_id] = new_request
            return ("1", new_request)

    def get_all_my_requests(self, user_id):
        """ get my requests """
        my_requests = requests.get(user_id, "0")
        if my_requests == "0":
            return "0"
        result = {}
        for request_title, req_dets in my_requests.iteritems():
            result[req_dets[0]] = {
                "title": request_title,
                "description": req_dets[1],
                "type": req_dets[2],
                "user_id": req_dets[3],
                "status": req_dets[4],
                "created_at": req_dets[5]
            }

        return ("1", result)

    def update(self, user_id, request_id, title, description, category):
        """ update request """
        my_requests = requests.get(user_id, "0")
        updated_at = time.strftime('%A %B, %d %Y %H:%M:%S')

        if my_requests == "0":
            result = ("0", "Request id not found.")
        else:
            for req_title, req_dets in my_requests.iteritems():
                if req_dets[0] == request_id:
                    update = ({title: (request_id, title, description, 
                                        category, user_id, req_dets[4], 
                                        req_dets[5], updated_at)})                                       
                    #check if it doesnt duplicate another request
                    matched_title = my_requests.get(title, "0")
                    if matched_title == "0":
                        my_requests.pop(req_title)
                        my_requests.update(update)
                        result = ("1", update)
                    else: 
                        if matched_title[0] == request_id:
                            my_requests.pop(req_title)
                            my_requests.update(update)
                            result = ("1", update)
                        else:
                            result = ("0", "Duplicate entry, request not updated")
                # else: 
                #     result = ("0", "Request id not found")
        return result
        
    @staticmethod
    def get_by_id(user_id, request_id):
        """ get request by id"""
        my_requests = requests.get(user_id, "0")
        
        if my_requests == "0":
            return ("0")
        for request_title, req_dets in my_requests.iteritems():
            if req_dets[0] == request_id:
                return ("1", request_title, req_dets)
        return ("0")
        
