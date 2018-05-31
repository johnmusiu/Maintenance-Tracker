"""
    defines the data models of the app
"""
import time

#initialize an empty requests list
requests = {}

class Request():
    """ the requests model """
    user_requests = {}

    def __init__(self, title, description, category):
        """initialize instance variables """
        self.title = title
        self.description = description
        self.category = category
        self.status = "open"
        self.created_at = time.strftime('%A %B, %d %Y %H:%M:%S')
    
    def save(self, user_id):
        """ save request """
        #get my requests
        my_requests = requests.get(user_id, "0")
        count = 0
        for user, user_requests in requests.iteritems():
            count += len(user_requests)
        new_request = ({self.title: (self.description, self.category,user_id, 
                                      self.status, self.created_at)})
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
        return my_requests

    @staticmethod
    def update(user_id, request_id, title, description, category):
        """ update request """
        my_requests = requests.get(user_id, "0")
        if my_requests == "0":
            result = ("0", "Request id not found.")
        else:
            for req_title, req_dets in my_requests.iteritems():
                if req_dets[0] == request_id:
                    update = ({title: (request_id, title, description, 
                                        category, user_id, req_dets[4], 
                                        req_dets[5])})
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
                else: 
                    result = ("0", "Request id not found")
            return result
        
    @staticmethod
    def get_by_id():
        """ get request by id"""
