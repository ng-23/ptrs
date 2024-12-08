from ptrs.app import utils
from ptrs.app.model import data_mappers, entities
from flask import Request, ctx
from abc import abstractmethod
from datetime import datetime, timedelta

# maps a Service class to a dict of {"name":str, "data_mappers":[DataMapper]}
registered_services = {}


def register_service(name: str, *data_mappers: data_mappers.SQLiteDataMapper):
    """
    Registers a Service class

    Registered Services can be used by Controllers and Views in the app
    """
    def decorator(service_class):
        if service_class in registered_services:
            raise ValueError(f"Service class {service_class} is already registered to a name and list of DataMappers")

        registered_services[service_class] = {
            "name": name,
            "data_mappers": list(data_mappers),
        }

        return service_class

    return decorator


class Service(utils.Observable):
    """
    Services are part of the Model layer. They define specific interactions between the domain objects and application logic.
    It is Services that provide the functionality for e.g. logging in to a web app or creating a new account. Naturally, they
    rely on other components in the Model layer to provide this functionality.

    Services need not know about or rely on components outside the Model layer. They are not expected to return anything.
    That said, in MVC, we allow certain external components like Views to "observe" Services and
    be notified of when/how they change the state of the Model. Otherwise, Services do their work largely in silence.
    """
    def __init__(self):
        self._app_ctx = None

    @property
    def app_ctx(self):
        return self._app_ctx

    @app_ctx.setter
    def app_ctx(self, app_ctx: ctx.AppContext):
        self._app_ctx = app_ctx

    @abstractmethod
    def change_state(self, request: Request, *args, **kwargs):
        pass


@register_service("create_pothole", data_mappers.PotholeMapper, data_mappers.WorkOrderMapper)
class CreatePothole(Service):
    def __init__(self, pothole_mapper: data_mappers.PotholeMapper, work_order_mapper: data_mappers.WorkOrderMapper):
        super().__init__()
        self._pothole_mapper = pothole_mapper
        self._work_order_mapper = work_order_mapper
        self._observers = []

    def register_observer(self, observer: utils.Observer):
        self._observers.append(observer)

    def notify_observers(self, model_state: utils.ModelState, *args, **kwargs):
        for observer in self._observers:
            observer.notify(model_state, *args, **kwargs)

    def change_state(self, request: Request, *args, **kwargs):
        self._pothole_mapper.db = self._app_ctx.db
        self._work_order_mapper.db = self._app_ctx.db

        if request.is_json and request.content_length > 0:
            request.json.update({
                "repair_status": "not repaired",
                "repair_type": "concrete" if request.json["size"] >= 8 else "asphalt",
                "repair_priority": ("major" if request.json["size"] >= 8 else "medium" if request.json["size"] >= 4 else "minor"),
                "report_date": datetime.now(),
                "expected_completion": datetime.now() + timedelta(2),
            })
            try:
                pothole = entities.Pothole(**request.json)
            except Exception as e:
                self.notify_observers(utils.ModelState(valid=False, message=str(e), errors=[e]))
            else:
                self.notify_observers(self._pothole_mapper.create(pothole), *args, **kwargs) # notify observers of successful pothole creation
                # silently create a new work order
                # TODO: in theory, this shouldn't fail...right?
                self._work_order_mapper.create(entities.WorkOrder(
                    pothole_id=pothole.pothole_id,
                    assignment_date=datetime.now(),
                    estimated_man_hours=1 if pothole.size < 3 else 3 if pothole.size < 7 else 5,
                ))
        else:
            self.notify_observers(
                utils.ModelState(
                    valid=False,
                    message=f"Request body must be of mimetype application/json and non-empty, "
                            f"got {request.mimetype} with length {request.content_length} instead",
                ),
            )


@register_service("read_potholes", data_mappers.PotholeMapper)
class ReadPotholes(Service):
    def __init__(self, pothole_mapper: data_mappers.PotholeMapper):
        super().__init__()
        self._pothole_mapper = pothole_mapper
        self._observers = []

    def register_observer(self, observer: utils.Observer):
        self._observers.append(observer)

    def notify_observers(self, model_state: utils.ModelState, *args, **kwargs):
        for observer in self._observers:
            observer.notify(model_state, *args, **kwargs)

    def change_state(self, request: Request, *args, **kwargs):
        self._pothole_mapper.db = self._app_ctx.db
        try:
            query_params, sort_params = utils.distill_query_params(request)
        except Exception as e:
            self.notify_observers(utils.ModelState(valid=False, message=str(e), errors=[e]))
        else:
            self.notify_observers(self._pothole_mapper.read(query_params=query_params, sort_params=sort_params))


@register_service("update_potholes", data_mappers.PotholeMapper)
class UpdatePotholes(Service):
    def __init__(self, pothole_mapper: data_mappers.PotholeMapper):
        super().__init__()
        self._pothole_mapper = pothole_mapper
        self._observers = []

    def register_observer(self, observer: utils.Observer):
        self._observers.append(observer)

    def notify_observers(self, model_state: utils.ModelState, *args, **kwargs):
        for observer in self._observers:
            observer.notify(model_state, *args, **kwargs)

    def change_state(self, request: Request, *args, **kwargs):
        self._pothole_mapper.db = self._app_ctx.db
        if request.is_json:
            try:
                query_params, _ = utils.distill_query_params(request) # sort params are unused here
            except Exception as e:
                self.notify_observers(utils.ModelState(valid=False, message=str(e), errors=[e]))
            else:
                self.notify_observers(self._pothole_mapper.update(query_params, request.json), *args, **kwargs)
        else:
            self.notify_observers(utils.ModelState(valid=False, message=f"Request body must be of mimetype application/json, got {request.mimetype} instead"))

@register_service("create_work_order", data_mappers.WorkOrderMapper)
class CreateWorkOrder(Service):
    def __init__(self, work_order_mapper: data_mappers.WorkOrderMapper):
        super().__init__()
        self._work_order_mapper = work_order_mapper
        self._observers = []

    def register_observer(self, observer: utils.Observer):
        self._observers.append(observer)

    def notify_observers(self, model_state: utils.ModelState, *args, **kwargs):
        for observer in self._observers:
            observer.notify(model_state, *args, **kwargs)

    def change_state(self, request: Request, *args, **kwargs):
        self._work_order_mapper.db = self._app_ctx.db
        if request.is_json and request.content_length > 0:
            request.json.update({
                "assignment_date": datetime.now(),
            })
            try:
                work_order = entities.WorkOrder(**request.json)
            except Exception as e:
                self.notify_observers(utils.ModelState(valid=False, message=str(e), errors=[e]))
            else:
                self.notify_observers(self._work_order_mapper.create(work_order), *args, **kwargs)
        else:
            self.notify_observers(
                utils.ModelState(
                    valid=False,
                    message=f"Request body must be of mimetype application/json and non-empty, "
                            f"got {request.mimetype} with length {request.content_length} instead",
                ),
            )


@register_service("read_work_orders", data_mappers.WorkOrderMapper, data_mappers.PotholeMapper)
class ReadWorkOrders(Service):
    def __init__(self, work_order_mapper: data_mappers.WorkOrderMapper, pothole_mapper: data_mappers.PotholeMapper):
        super().__init__()
        self._work_order_mapper = work_order_mapper
        self._pothole_mapper = pothole_mapper
        self._observers = []

    def register_observer(self, observer: utils.Observer):
        self._observers.append(observer)

    def notify_observers(self, model_state: utils.ModelState, *args, **kwargs):
        for observer in self._observers:
            observer.notify(model_state, *args, **kwargs)

    def change_state(self, request: Request, *args, **kwargs):
        self._work_order_mapper.db = self._app_ctx.db
        self._pothole_mapper.db = self._app_ctx.db

        try:
            query_params, sort_params = utils.distill_query_params(request)
        except Exception as e:
            self.notify_observers(utils.ModelState(valid=False, message=str(e), errors=[e]))
        else:
            model_state = self._work_order_mapper.read(query_params=query_params, sort_params=sort_params)
            if not model_state.valid:
                self.notify_observers(model_state)
                return
            og_msg = model_state.message
            
            # must have succesfully read some work orders
            # also grab the pothole information associated with each one
            data = []
            for work_order in model_state.data:
                model_state = self._pothole_mapper.read(query_params={'pothole_id': {'filter':'=', 'val':work_order.pothole_id}})
                if not model_state.valid:
                    # TODO: this shouldn't happen ever...right?
                    self.notify_observers(model_state)
                    return
                pothole = model_state.data[0] # succesfully read a pothole, get it from the model state
                work_order_dict = work_order.to_json() # jsonify work order
                work_order_dict['pothole'] = pothole.to_json() # add new key:val pair for jsonified pothole
                data.append(work_order_dict)

            self.notify_observers(utils.ModelState(valid=True, message=og_msg, data=data))


@register_service("update_work_order", data_mappers.WorkOrderMapper)
class UpdateWorkOrders(Service):
    def __init__(self, work_order_mapper: data_mappers.WorkOrderMapper):
        super().__init__()
        self._work_order_mapper = work_order_mapper
        self._observers = []

    def register_observer(self, observer: utils.Observer):
        self._observers.append(observer)

    def notify_observers(self, model_state: utils.ModelState, *args, **kwargs):
        for observer in self._observers:
            observer.notify(model_state, *args, **kwargs)

    def change_state(self, request: Request, *args, **kwargs):
        self._work_order_mapper.db = self._app_ctx.db
        if request.is_json:
            try:
                query_params, _ = utils.distill_query_params(request) # sort params are unused here
            except Exception as e:
                self.notify_observers(utils.ModelState(valid=False, message=str(e), errors=[e]))
            else:
                self.notify_observers(self._work_order_mapper.update(query_params, request.json), *args, **kwargs)
        else:
            self.notify_observers(utils.ModelState(valid=False, message=f"Request body must be of mimetype application/json, got {request.mimetype} instead"))


@register_service("read_report", data_mappers.ReportMapper)
class ReadReport(Service):
    def __init__(self, report_mapper: data_mappers.ReportMapper):
        super().__init__()
        self._report_mapper = report_mapper
        self._observers = []

    def register_observer(self, observer: utils.Observer):
        self._observers.append(observer)

    def notify_observers(self, model_state: utils.ModelState, *args, **kwargs):
        for observer in self._observers:
            observer.notify(model_state, *args, **kwargs)

    def change_state(self, request: Request, *args, **kwargs):
        self._report_mapper.db = self._app_ctx.db
        try:
            query_params, sort_params = utils.distill_query_params(request)
        except Exception as e:
            self.notify_observers(utils.ModelState(valid=False, message=str(e), errors=[e]))
        else:
            self.notify_observers(self._report_mapper.read(query_params=query_params, sort_params=sort_params))

