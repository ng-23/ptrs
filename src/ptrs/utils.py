from typing import List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# code largely from Python example in Wikipedia page about observer pattern
# see https://en.wikipedia.org/wiki/Observer_pattern
class Observer(ABC):
    def notify(self, *args, **kwargs):
        pass

class Observerable(ABC):
    @abstractmethod
    def register_observer(self, observer:Observer):
        pass

    @abstractmethod
    def notify_observers(self, *args, **kwargs):
        pass

@dataclass(frozen=True)
class ModelState():
    '''
    Represents the state of the Model layer after the processing of a request by the user

    Intended to be consumed by an Observer of a Service (e.g. a View) for further processing
    '''

    valid: bool = False
    message: str = ''
    data: any = None
    errors: List[Exception] = field(default_factory=list) # see https://stackoverflow.com/questions/53632152/why-cant-dataclasses-have-mutable-defaults-in-their-class-attributes-declaratio

