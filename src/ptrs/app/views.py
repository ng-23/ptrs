from ptrs.utils import Observer, ModelState
from ptrs.app.model import services, entities
from flask import Response, jsonify
from abc import abstractmethod

registered_views = {}  # maps a View class to a dict of {'name':str, 'service':Service}


def register_view(name: str, service: services.Service):
    """
    Registers a View class

    Registered Views can be used by Controllers in the app
    """

    def decorator(view_class):
        if view_class in registered_views:
            raise ValueError(
                f"View class {view_class} is already registered to a name and Service"
            )

        registered_views[view_class] = {"name": name, "service": service}

        return view_class

    return decorator


class View(Observer):
    def __init__(self):
        self._model_state = None

    @property
    def model_state(self):
        return self._model_state

    @model_state.setter
    def model_state(self, model_state: ModelState):
        self._model_state = model_state

    @abstractmethod
    def format_response(self, *args, **kwargs) -> Response:
        pass


@register_view("create_pothole", services.CreatePothole)
class CreatePothole(View):
    def __init__(self, service: services.CreatePothole):
        super().__init__()
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> tuple[Response, int]:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {}
        if self._model_state.data is not None:
            data = self._model_state.data
            if isinstance(data, entities.Entity):
                data = data.to_json()

        if status == 404:
            data["message"] = self._model_state.message

        return jsonify(**data), status

    def notify(self, model_state: ModelState):
        self.model_state = model_state


@register_view("read_potholes", services.ReadPotholes)
class ReadPotholes(View):
    def __init__(self, service: services.ReadPotholes):
        super().__init__()
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> tuple[Response, int]:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {}
        if self._model_state.data is not None:
            data = self._model_state.data
            if isinstance(data, entities.Entity):
                data = data.to_json()
            elif isinstance(data, list):
                data = {"potholes": [item.to_json() for item in data]}

        if status == 404:
            data["message"] = self._model_state.message

        return jsonify(**data), status

    def notify(self, model_state: ModelState):
        self.model_state = model_state


@register_view("create_work_order", services.CreateWorkOrder)
class CreateWorkOrder(View):
    def __init__(self, service: services.CreateWorkOrder):
        super().__init__()
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> tuple[Response, int]:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {}
        if self._model_state.data is not None:
            data = self._model_state.data
            if isinstance(data, entities.Entity):
                data = data.to_json()

        if status == 404:
            data["message"] = self._model_state.message

        return jsonify(**data), status

    def notify(self, model_state: ModelState):
        self.model_state = model_state


@register_view("update_work_order", services.UpdateWorkOrder)
class UpdateWorkOrder(View):
    def __init__(self, service: services.UpdateWorkOrder):
        super().__init__()
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> tuple[Response, int]:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {}
        if self._model_state.data is not None:
            data = self._model_state.data
            if isinstance(data, entities.Entity):
                data = data.to_json()

        if status == 404:
            data["message"] = self._model_state.message

        return jsonify(**data), status

    def notify(self, model_state: ModelState):
        self.model_state = model_state


@register_view("read_work_orders", services.ReadWorkOrders)
class ReadWorkOrders(View):
    def __init__(self, service: services.ReadWorkOrders):
        super().__init__()
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> tuple[Response, int]:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {}
        if self._model_state.data is not None:
            data = self._model_state.data
            if isinstance(data, entities.Entity):
                data = data.to_json()
            elif isinstance(data, list):
                data = {"work_orders": [item.to_json() for item in data]}

        if status == 404:
            data["message"] = self._model_state.message

        return jsonify(**data), status

    def notify(self, model_state: ModelState):
        self.model_state = model_state
