from ptrs.app import views
from ptrs.app import database
from ptrs.app.model import services
from flask.views import View
from flask import request, Request, g
from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta

# maps a Controller class to a dict of {'name':str, 'service':Service, 'view':View}
# registered Controllers can be assigned routes in the app, allowing the user to interact with them
# just because a Controller is registered does not mean it is routable - routes must be assigned separately
registered_controllers = {}


def register_controller(name: str, service: services.Service, view: views.View):
    def decorator(controller_class: Controller):
        if controller_class in registered_controllers:
            raise ValueError(
                f"Controller class {controller_class} is already registered to a name, Service, and View."
            )

        registered_controllers[controller_class] = {
            "name": name,
            "service": service,
            "view": view,
        }

        return controller_class

    return decorator


# maps a tuple of (url_rule:str, req_method:str) to a dict of {'endpoint':str, 'controller_class':Controller, 'service_class':Service, 'view_class':View}
# all routable Controllers are registered, but not all registered Controllers are routable
# making a Controller routable allows the user to interact with it via HTTP request methods sent to the app
routable_controllers = {}


def register_routable_controller(url_rule: str, req_method: str):
    def decorator(controller_class: Controller):
        if (url_rule, req_method) in routable_controllers:
            raise ValueError(
                f"There is already a Controller associated with the URL rule {url_rule} and request method {req_method}"
            )

        if controller_class not in registered_controllers:
            raise ValueError(f"{controller_class} is not registered as a Controller")

        controller_vars = registered_controllers[controller_class]

        routable_controllers[(url_rule, req_method)] = {
            "endpoint": controller_vars["name"],
            "controller_class": controller_class,
            "service_class": controller_vars["service"],
            "view_class": controller_vars["view"],
        }

        return controller_class

    return decorator


class Controller(ABC, View):
    """
    Flask has its own interpretation of the term View that
    differs slightly from its meaning in MVC.

    In MVC, the View encapsulates the logic for returning a
    response to the user. It interacts with components in the
    Model to get the data it needs to format into a response.

    In Flask, a View is anything that receives an HTTP request
    and sends an HTTP response in return. This is a much looser
    definition and in practice I'd argue Flask Views are closer
    to Controllers in MVC.

    For this system, we define Controllers to be Flask Views,
    which allows Flask to take care of mapping API routes to them and us to
    define their behavior more in line with the MVC definition.
    """

    @abstractmethod
    def dispatch_request(self):
        pass

    @staticmethod
    def calc_repair(request: Request):
        request.json["repair_status"] = "Not Repaired"
        request.json["repair_type"] = (
            "concrete" if request.json["size"] >= 8 else "asphalt"
        )
        request.json["repair_priority"] = (
            "major"
            if request.json["size"] >= 8
            else "medium" if request.json["size"] >= 4 else "minor"
        )
        request.json["report_date"] = (
            f'{datetime.now().strftime("%I:%M%p ") + date.today().strftime("%B %d, %Y")}'
        )
        request.json["expected_completion"] = (
            f'{(date.today() + timedelta(2)).strftime("%B %d, %Y")}'
        )


@register_routable_controller("/pothole/", "POST")
@register_controller("create_pothole", services.CreatePothole, views.CreatePothole)
class CreatePothole(Controller):
    methods = ["POST"]

    def __init__(
            self, service: services.CreatePothole, view: views.CreatePothole
    ) -> None:
        self._service = service
        self._view = view

    def dispatch_request(self):
        database.get_db()  # add a database connection to the current app/request context
        self._service.app_ctx = g  # point the Service to the current app/request context, from which it can get e.g. database connection
        self.calc_repair(request)
        self._service.change_state(
            request
        )  # tell Service to process user's request and change state of Model layer
        return self._view.format_response()


@register_routable_controller("/potholes/", "GET")
@register_controller("read_potholes", services.ReadPotholes, views.ReadPotholes)
class ReadPotholes(Controller):
    methods = ["GET"]

    def __init__(
            self, service: services.ReadPotholes, view: views.ReadPotholes
    ) -> None:
        self._service = service
        self._view = view

    def dispatch_request(self):
        database.get_db()
        self._service.app_ctx = g
        self._service.change_state(request)
        return self._view.format_response()
