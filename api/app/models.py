"""
    defines the data models of the app
"""
import time

#initialize an empty requests list
requests = {}

class Request():
    """ the requests model """

    def __init__(self, title, description, category):
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
        for user, user_requests in requests.iteritems():
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
        return my_requests

    def update(self):
        """ update request """
        # for req in self.requests:
        #     if req['title']


    @staticmethod
    def get_by_id():
        """ get request by id"""
