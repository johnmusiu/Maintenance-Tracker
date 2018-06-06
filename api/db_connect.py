"""
    module to initialize db connections 
    and close them
"""
import psycopg2
from instance.secret import DB_USER, DB_PASSWORD
from instance.config import app_config

class DBConnect():
    def __init__(self):
        """initialize db instance"""
        self.conn = ""
        self.cursor = ""

    def connect(self):
        """ create a db conn object """
        db_name = app_config['development'].DB_NAME
        try:
            self.conn = psycopg2.connect(dbname=db_name, 
                                          user=DB_USER, 
                                          host='localhost', 
                                          password=DB_PASSWORD)
            self.cursor = self.conn.cursor()
            return self.cursor
        except:
            return False

    def close_conn(self):
        """ close cursor and db connection """
        self.cursor.close()
        self.conn.close()

print(app_config['development'].DB_NAME)