"""
    module to initialize db connections 
    and close them
"""
import os
import psycopg2

class DBConnect():
    def __init__(self):
        """initialize db instance"""

    def connect(self):
        """ create a db conn object """
        try:
            self.conn = psycopg2.connect(dbname=os.getenv("DB_NAME"), 
                                          user=os.getenv("DB_USER"), 
                                          host='localhost', 
                                          password=os.getenv("DB_PASSWORD"))
            self.cursor = self.conn.cursor()
            return self.cursor
        except:
            return False

    def close_conn(self):
        """ close cursor and db connection """
        self.cursor.close()
        self.conn.close()
