""" defines db migrations

    create DB, create tables
"""
import os
from api.db_connect import DBConnect

def migration():
    try:
        db = DBConnect()
        cursor= db.connect()

        if cursor is not False:
            #drop db if exists
            # cursor.execute("DROP DATABASE IF EXISTS "+ os.getenv('DB_NAME'))
            
            #create db
            # cursor.execute("CREATE DATABASE "+ os.getenv('DB_NAME'))
            
            #drop tables if they exist
            cursor.execute("DROP TABLE IF EXISTS users;")
            cursor.execute("DROP TABLE IF EXISTS requests;")
            
            #create table user sql statement
            cursor.execute("CREATE TYPE is_admin AS ENUM('0', '1');")
            create_users = """CREATE TABLE users( 
                                    user_id SERIAL PRIMARY KEY,
                                    first_name VARCHAR(25),
                                    last_name  VARCHAR(25),
                                    email VARCHAR(25) UNIQUE,
                                    password VARCHAR(255),
                                    created_at TIMESTAMP,
                                    last_seen TIMESTAMP,
                                    is_admin is_admin
                            );"""

            #create table requests sql statement
            cursor.execute("CREATE TYPE status AS ENUM('unresolved', 'ongoing', 'resolved');")
            cursor.execute("CREATE TYPE req_type AS ENUM('repair', 'maintenance');")
            create_requests = """CREATE TABLE requests(
                                    request_id SERIAL PRIMARY KEY,
                                    user_id INT,
                                    admin_id INT,
                                    status status,
                                    type req_type,
                                    title VARCHAR(60),
                                    description TEXT,
                                    created_at TIMESTAMP,
                                    updated_at TIMESTAMP,
                                    resolved_at TIMESTAMP
                            ); """

            cursor.execute(create_users)
            cursor.execute(create_requests)
            print("Migrations done successfully!")
            db.close_conn()
            return True
    except:
        print("Error migrating tables")
        return False


migration()