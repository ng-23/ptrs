from ptrs.app.utils import Observer, ModelState
from ptrs.app.model import services, entities
from flask import Response, jsonify, render_template, make_response
from abc import abstractmethod
from xhtml2pdf import pisa
from io import BytesIO
from datetime import date, timedelta

registered_views = {}  # maps a View class to a dict of {"name":str, "service":Service}


def register_view(name: str, service: services.Service):
    """
    Registers a View class

    Registered Views can be used by Controllers in the app
    """
    def decorator(view_class):
        if view_class in registered_views:
            raise ValueError(f"View class {view_class} is already registered to a name and Service")

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

        data = {"message": self._model_state.message, "data": []}

        for item in self._model_state.data:
            if isinstance(item, entities.Entity):
                data["data"].append(item.to_json())
            else:
                data["data"].append(item)

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

        data = {"message": self._model_state.message, "data": []}

        for item in self._model_state.data:
            if isinstance(item, entities.Entity):
                data["data"].append(item.to_json())
            else:
                data["data"].append(item)

        # TODO Fix
        for pothole in data["data"]:
            pothole["report_date"] = pothole["report_date"][:19]
            pothole["expected_completion"] = pothole["expected_completion"][:10]
            if pothole["actual_completion"] is not None:
                pothole["actual_completion"] = pothole["actual_completion"][:10]

        return jsonify(**data), status

    def notify(self, model_state: ModelState):
        self.model_state = model_state


@register_view("update_potholes", services.UpdatePotholes)
class UpdatePotholes(View):
    def __init__(self, service: services.UpdatePotholes):
        super().__init__()
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> tuple[Response, int]:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {"message": self._model_state.message, "data": []}

        for item in self._model_state.data:
            if isinstance(item, entities.Entity):
                data["data"].append(item.to_json())
            else:
                data["data"].append(item)

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

        data = {"message": self._model_state.message, "data": []}

        for item in self._model_state.data:
            if isinstance(item, entities.Entity):
                data["data"].append(item.to_json())
            else:
                data["data"].append(item)

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

        data = {"message": self._model_state.message, "data": []}

        for item in self._model_state.data:
            if isinstance(item, entities.Entity):
                data["data"].append(item.to_json())
            else:
                data["data"].append(item)

        # TODO Fix
        for work_order in data["data"]:
            work_order["pothole"]["report_date"] = work_order["pothole"]["report_date"][:19]
            work_order["assignment_date"] = work_order["assignment_date"][:10]
            work_order["pothole"]["expected_completion"] = work_order["pothole"]["expected_completion"][:10]
            if work_order["pothole"]["actual_completion"] is not None:
                work_order["pothole"]["actual_completion"] = work_order["pothole"]["actual_completion"][:10]

        return jsonify(**data), status

    def notify(self, model_state: ModelState):
        self.model_state = model_state


@register_view("update_work_orders", services.UpdateWorkOrders)
class UpdateWorkOrders(View):
    def __init__(self, service: services.UpdateWorkOrders):
        super().__init__()
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> tuple[Response, int]:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {"message": self._model_state.message, "data": []}

        for item in self._model_state.data:
            if isinstance(item, entities.Entity):
                data["data"].append(item.to_json())
            else:
                data["data"].append(item)

        return jsonify(**data), status

    def notify(self, model_state: ModelState):
        self.model_state = model_state


@register_view("read_work_orders", services.ReadReport)
class ReadReport(View):
    def __init__(self, service: services.ReadReport):
        super().__init__()
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> Response:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {"message": self._model_state.message, "data": []}

        for item in self._model_state.data:
            if isinstance(item, entities.Entity):
                data["data"].append(item.to_json())
            else:
                data["data"].append(item)

        # TODO Fix
        for work_order in data["data"]:
            work_order["pothole"]["report_date"] = work_order["pothole"]["report_date"][:19]
            work_order["assignment_date"] = work_order["assignment_date"][:10]
            work_order["pothole"]["expected_completion"] = work_order["pothole"]["expected_completion"][:10]
            if work_order["pothole"]["actual_completion"] is not None:
                work_order["pothole"]["actual_completion"] = work_order["pothole"]["actual_completion"][:10]

        # TODO Might belong in services
        pdf = BytesIO()
        report = render_template(
            "report.html",
            work_orders=data["data"],
            assigned_work_orders=len(data["data"]),
            on_time_work_orders=sum(work_order["pothole"]["expected_completion"] > work_order["pothole"]["actual_completion"] for work_order in data["data"] if
                                    work_order["pothole"]["actual_completion"] is not None),
            complete_work_orders=sum(work_order["pothole"]["repair_status"] in ["repaired", "removed", "temporarily repaired"] for work_order in data["data"]),
            incomplete_work_orders=sum(work_order["pothole"]["repair_status"] == "not repaired" for work_order in data["data"]),
            report_start_date=(date.today() - timedelta(days=date.today().weekday() + 1)).strftime("%B %d, %Y"),
            report_end_date=(date.today() + timedelta(days=5 - date.today().weekday())).strftime("%B %d, %Y")
        )
        pisa.CreatePDF(report, pdf)

        response = make_response(pdf.getvalue(), status)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

        return response

    def notify(self, model_state: ModelState):
        self.model_state = model_state