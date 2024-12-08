import os
from ptrs.app import database
from flask import Flask, render_template
from dotenv import load_dotenv

"""
When you import the ptrs.app package,
all code in this module will be run automatically.
"""

API_ROUTE_PREFIX = "/api" # prepend this to any route that is intended to act as a REST API endpoint
API_FILTERS = {'gt':'>','lt':'<','gte':'>=','lte':'<='}
API_SORT_BY_PARAM = "sort_by" # denotes the name of the query string parameter that indicates sorting
API_SORT_OPERATORS = {"+":'ASC',"-":'DESC'} # if present in the part of the query string following the sort by param, these indicate the sort method

# load environment variables, which we'll use to configure the app
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = os.getenv("DATABASE")

    with app.app_context():
        database.init_db(
            os.getenv("DATABASE_SCHEMA")
        )  # this creates the database according to the provided schema and saves it to the provided location

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route("/about/")
    def about():
        return render_template('about.html')

    @app.route("/potholes/")
    def potholes():
        return render_template("potholes.html")

    @app.route("/work-orders/")
    def work_orders():
        return render_template("work-orders.html")

    return app
