from abc import ABC, abstractmethod

from model import Model


class View(ABC):
    """Abstract view class"""
    _controller = None

    def __init__(self, controller):
        self._controller = controller

    @abstractmethod
    def render(self, model: Model):
        """Render the view"""

    @abstractmethod
    def cleanup(self):
        """Cleanup all resources before shutting down"""
