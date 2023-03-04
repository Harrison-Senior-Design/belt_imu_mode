from abc import ABC, abstractmethod

from model import Model

class View(ABC):
    _controller = None
    
    def __init__(self, controller):
        self._controller = controller

    @abstractmethod
    def render(self, model: Model):
        pass

    @abstractmethod
    def cleanup(self):
        pass
        
    @abstractmethod
    def update(self):
        pass
