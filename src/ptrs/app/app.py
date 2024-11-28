from flask import Flask
from ptrs.app.model import services
from ptrs.app import controllers, create_app

"""
This module creates a Flask instance, 
effectively launching the app.

If you run this module directly (e.g. python app.py),
the default Flask WSGI server will be used.
This WSGI server is incredibly basic and meant for
development only - do not use it in a producting setting.

If you run this module through a proper WSGI server (e.g. gunicorn),
that WSGI server will be used instead of Flask's default one.
"""


def add_routable_controllers(flask_app: Flask):
    """
    A routable Controller is a Controller with an API route assigned to it
    These Controllers are intended to be interacted with by the user via HTTP request methods
    To allow Flask to route requests to these Controllers, they must be added to the app instance
    """

    for (
            url_rule,
            req_method,
    ), controller_vars in controllers.routable_controllers.items():
        data_mappers = [
            data_mapper_class()
            for data_mapper_class in services.registered_services[
                controller_vars["service_class"]
            ]["data_mappers"]
        ]  # instantiate DataMappers the Controller's Service depends on
        service = controller_vars["service_class"](
            *data_mappers
        )  # instantiate the Service the Controller and its View depend on
        view = controller_vars["view_class"](
            service
        )  # instantiate the View the Controller depends on
        service.register_observer(
            view
        )  # View now observes the Service, so it will be notified by the Service when the Service changes the Model's state

        # see https://stackoverflow.com/questions/19261833/what-is-an-endpoint-in-flask
        # to understand how Flask defines and manages routes
        flask_app.add_url_rule(
            url_rule,
            endpoint=controller_vars["endpoint"],
            view_func=controller_vars["controller_class"].as_view(
                controller_vars["endpoint"], service, view
            ),
        )


app = create_app()
add_routable_controllers(app)

if __name__ == "__main__":
    # executed when running module directly
    # this will use the basic (insecure) Flask WSGI server
    app.run(debug=True)
else:
    # executed when not running module directly
    # e.g. through a proper third-party WSGI server
    pass
