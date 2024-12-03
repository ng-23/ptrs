import os
from ptrs.app import controllers, database
from ptrs.app.model import services
from flask import Flask, render_template
from dotenv import load_dotenv

"""
When you import the ptrs.app package,
all code in this module will be run automatically.
"""

# load environment variables, which we'll use to configure the app
load_dotenv()


def add_routable_controllers(app: Flask):
    """
    A routable Controller is a Controller with an API route assigned to it
    These Controllers are intended to be interacted with by the user via HTTP request methods
    To allow Flask to route requests to these Controllers, they must be added to the app instance
    """
    for (url_rule, req_method), controller_vars in controllers.routable_controllers.items():
        data_mappers = [
            data_mapper_class()
            for data_mapper_class in services.registered_services[controller_vars["service_class"]]["data_mappers"]
        ]  # instantiate DataMappers the Controller's Service depends on
        service = controller_vars["service_class"](*data_mappers)  # instantiate the Service the Controller and its View depend on
        view = controller_vars["view_class"](service)  # instantiate the View the Controller depends on
        service.register_observer(view)  # View now observes the Service, so it will be notified by the Service when the Service changes the Model's state

        # see https://stackoverflow.com/questions/19261833/what-is-an-endpoint-in-flask
        # to understand how Flask defines and manages routes
        app.add_url_rule(
            url_rule,
            endpoint=controller_vars["endpoint"],
            view_func=controller_vars["controller_class"].as_view(controller_vars["endpoint"], service, view)
        )


def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = os.getenv("DATABASE")
    add_routable_controllers(app)

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
