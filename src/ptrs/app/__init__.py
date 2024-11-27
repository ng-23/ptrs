import os
from flask import Flask, render_template
from dotenv import load_dotenv
from ptrs.app import database

"""
When you import the ptrs.app package,
all code in this module will be run automatically.
"""

# load environment variables, which we'll use to configure the app
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = os.getenv("DATABASE")

    with app.app_context():
        database.init_db(
            os.getenv("DATABASE_SCHEMA")
        )  # this creates the database according to the provided schema and saves it to the provided location

    @app.route("/about")
    def about():
        return "Pothole Tracking and Repair System (PTRS)"

    @app.route("/pothole")
    def pothole():
        return render_template("pothole.html")

    return app
