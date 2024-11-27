from flask import Response
from abc import abstractmethod
from ptrs.utils import Observer
from ptrs.app.model import services

registered_views = {}  # maps a View class to a dict of {'name':str, 'service':Service}


def register_view(name: str, service: services.Service):
    def decorator(view_class):
        if view_class in registered_views:
            raise ValueError(
                f"View class {view_class} is already registered to a name and Service"
            )

        registered_views[view_class] = {"name": name, "service": service}

        return view_class

    return decorator


class View(Observer):
    @abstractmethod
    def format_response(self, *args, **kwargs) -> Response:
        pass


@register_view("create_pothole", services.CreatePothole)
class CreatePothole(View):
    def __init__(self, service: services.CreatePothole):
        self._service = service

    def format_response(self, *args, **kwargs) -> Response:
        return super().format_response(*args, **kwargs)

    def notify(self, *args, **kwargs):
        return super().notify(*args, **kwargs)


@register_view("read_potholes", services.ReadPotholes)
class ReadPotholes(View):
    def __init__(self, service: services.ReadPotholes):
        self._service = service

    def format_response(self, *args, **kwargs) -> Response:
        return super().format_response(*args, **kwargs)

    def notify(self, *args, **kwargs):
        return super().notify(*args, **kwargs)
