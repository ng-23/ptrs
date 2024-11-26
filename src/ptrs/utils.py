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

