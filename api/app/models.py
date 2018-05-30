"""
    defines the data models of the app
"""
class Request():
    """ the requests model """
    requests = []

    def __init__(self, title, description, category):
        self.request = {
            'id': 1,
            'title': title,
            'description': description,
            'category': category
        }
    
    def save(self):
        """ save request """
        self.requests.append(self.request)
        return self.request
        
    def update(self):
        """ update request """
        # for req in self.requests:
        #     if req['title']

    
    @staticmethod
    def get_all():
        """ get all requests"""
    

    @staticmethod
    def get_by_id():
        """ get request by id"""
