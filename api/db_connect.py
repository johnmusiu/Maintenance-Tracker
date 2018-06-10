"""
    module to initialize db connections
    and close them
"""
import os
import psycopg2


class DBConnect():
    """ class contains db connection URL """
    def __init__(self):
        """initialize db instance"""

    def connect(self):
        """ create a db conn object """
        try:
            if os.getenv("FLASK_CON") == "development":
                self.conn = psycopg2.connect(
                                 dbname=os.getenv("DB_NAME"),
                                 user=os.getenv("DB_USER"),
                                 host='localhost',
                                 password=os.getenv("DB_PASSWORD"))
            elif os.getenv("FLASK_CON") == "production":
                self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
            self.cursor = self.conn.cursor()
            return self.cursor
        except Exception:
            return False

    def close_conn(self):
        """ close cursor and db connection """
        self.cursor.close()
        self.conn.close()
