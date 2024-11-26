import os
from flask import Flask
from dotenv import load_dotenv
from ptrs.app.database import db

'''
When you import the ptrs.app package,
all code in this module will be run automatically.
'''

# load environment variables, which we'll use to configure the app
load_dotenv() 

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = os.getenv('DATABASE')

    with app.app_context():
        db.init_db(schema=os.getenv('DATABASE_SCHEMA')) # this adds a database connection to the app instance

    @app.route('/about')
    def about():
        return 'Pothole Tracking and Repair System (PTRS)'
        
    return app