from flask import Response, jsonify
from abc import abstractmethod
from ptrs.utils import Observer, ModelState
from ptrs.app.model import services, entities

registered_views = {} # maps a View class to a dict of {'name':str, 'service':Service}

def register_view(name:str, service:services.Service):
    '''
    Registers a View class

    Registered Views can be used by Controllers in the app
    '''
    def decorator(view_class):
        if view_class in registered_views:
            raise ValueError(f'View class {view_class} is already registered to a name and Service')
        
        registered_views[view_class] = {'name':name, 'service':service}

        return view_class
    
    return decorator

class View(Observer):
    @property
    def model_state(self):
        return self._model_state

    @model_state.setter
    def model_state(self, model_state:ModelState):
        self._model_state = model_state

    @abstractmethod
    def format_response(self, *args, **kwargs) -> Response:
        pass

@register_view('create_pothole', services.CreatePothole)
class CreatePothole(View):
    def __init__(self, service: services.CreatePothole):
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> Response:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {}
        if self._model_state.data is not None:
            data = self._model_state.data
            if isinstance(data, entities.Entity):
                data = data.to_json()             

        if status == 404:
            data['message'] = self._model_state.message

        return jsonify(**data), status

    def notify(self, model_state:ModelState):
        self.model_state = model_state

@register_view('read_potholes', services.ReadPotholes)  
class ReadPotholes(View):
    def __init__(self, service: services.ReadPotholes):
        self._service = service
        self.model_state = None

    def format_response(self, *args, **kwargs) -> Response:
        status = 200
        if not self._model_state.valid:
            status = 404

        data = {}
        if self._model_state.data is not None:
            data = self._model_state.data
            if isinstance(data, entities.Entity):
                data = data.to_json()
            elif isinstance(data, list):
                data = {'potholes':[item.to_json() for item in data]}

        if status == 404:
            data['message'] = self._model_state.message

        return jsonify(**data), status

    def notify(self, model_state:ModelState):
        self.model_state = model_state