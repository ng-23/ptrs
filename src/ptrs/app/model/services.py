from abc import abstractmethod
from flask import Request, ctx
from ptrs.utils import Observer, Observerable
from ptrs.app.model import data_mappers, entities

registered_services = {} # maps a Service class to a dict of {'name':str, 'data_mappers':[DataMapper]}

def register_service(name:str, *data_mappers:(data_mappers.SQLiteDataMapper)):
    def decorator(service_class):
        if service_class in registered_services:
            raise ValueError(f'Service class {service_class} is already registered to a name and list of DataMappers')
        
        registered_services[service_class] = {'name':name, 'data_mappers':list(data_mappers)}

        return service_class
    
    return decorator

class Service(Observerable):
    '''
    Services are part of the Model layer. They define specific interactions between the domain objects and application logic.
    It is Services that provide the functionality for e.g. logging in to a web app or creating a new account. Naturally, they
    rely on other components in the Model layer to provide this functionality. 

    Services need not know about or rely on components outside the Model layer. They are not expected to return anything.
    That said, in MVC, we allow certain external components like Views to "observe" Services and 
    be notified of when/how they change the state of the Model. Otherwise, Services do their work largely in silence.
    '''

    @property
    def db(self):
        self._app_ctx = self

    @db.setter
    def app_ctx(self, app_ctx:ctx.AppContext):
        self._app_ctx = app_ctx
    
    @abstractmethod
    def change_state(self, request:Request, *args, **kwargs) -> None:
        pass

@register_service('create_pothole', data_mappers.PotholeMapper)
class CreatePothole(Service):
    def __init__(self, pothole_mapper:data_mappers.PotholeMapper):
        self._pothole_mapper = pothole_mapper
        self._observers = []

    def register_observer(self, observer:Observer):
        self._observers.append(observer)
    
    def notify_observers(self, *args, **kwargs):
        return super().notify_observers(*args, **kwargs)

    def change_state(self, request:Request, *args, **kwargs):
        self._pothole_mapper.db = self._app_ctx.db
        return self._pothole_mapper.create(entities.Pothole('Oak St', 5, 'right_lane', 'asphalt', 'major'))
    
@register_service('read_potholes', data_mappers.PotholeMapper)
class ReadPotholes(Service):
    def __init__(self, pothole_mapper:data_mappers.PotholeMapper):
        self._pothole_mapper = pothole_mapper
        self._observers = []

    def register_observer(self, observer: Observer):
        self._observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        return super().notify_observers(*args, **kwargs)
    
    def change_state(self, request:Request, *args, **kwargs) -> None:
        self._pothole_mapper.db = self._app_ctx.db
        return self._pothole_mapper.read_by_id(request.view_args['id'])