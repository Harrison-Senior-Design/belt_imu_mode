import threading

class SharedDataClass():
    _instance = None
    _lock = threading.Lock()
    angle = 30

    def __new__(cls):
        if cls._instance is None: 
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        
        return cls._instance
    
    def update_value(self, value):
        with self._lock:
            self.angle = value