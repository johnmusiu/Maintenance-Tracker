import os
import getpass
from api.db_connect import DBConnect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("""
    Let's setup a db to run the project on
                *****       *****
                    ********
                      ***
    But first we need your password for psql user:  postgres

""")
password = getpass.getpass('Enter your password for db user **postgres**: \n')
os.environ['DB_PASSWORD'] = password
os.environ['DB_NAME'] = 'postgres'

db = DBConnect()
cursor = db.connect()
db.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

db_name = input("Enter a DB name for use in this application:\n")
db_name_test = db_name+"_tests"

os.environ['DB_NAME'] = db_name
os.environ['DB_TEST'] = db_name_test

try:
    cursor.execute("CREATE DATABASE "+ db_name)
    cursor.execute("CREATE DATABASE "+ db_name_test)
    db.conn.commit()
    db.close_conn()
    file_env = open('.env', 'a+')
    file_env.write("export DB_NAME='"+db_name+"'\n")
    file_env.write("export DB_TEST='"+db_name_test+"'\n")
    file_env.write("export DB_PASSWORD='"+password+"'\n")
    file_env.close()
    print("Databases created successfully. \n 1: testing & 2: live ")
    print("Added DB_NAME and DB_PASSWORD to .env file\n\n\n")
    print("run 'source .env' to set environment variables\n\n\n")
    print("Goodbye")
except Exception as ex:
    print("***************Error*************")
    print(ex)
    


