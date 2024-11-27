from abc import ABC, abstractmethod


class Observer(ABC):
    def notify(self, *args, **kwargs):
        pass


class Observerable(ABC):
    @abstractmethod
    def register_observer(self, observer: Observer):
        pass

    @abstractmethod
    def notify_observers(self, *args, **kwargs):
        pass
