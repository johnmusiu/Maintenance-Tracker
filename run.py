"""
    Defines the entry point through which to start our app 
"""
import os
from api import create_app

config_name = os.getenv('APP_SETTINGS') 
app = create_app(config_name)

if __name__ == '__main__':
    app.run()