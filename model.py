from controller import Controller

class Model():
    _direction_index = 0
    _initial_offset = 0
    _directions = []
    _controller = None
    _current_facing = 0
    
    def __init__(self, controller: Controller):
        self._belt_controller = controller

    def set_current_facing(self, dir: int) -> None:
        self._current_facing = dir

    def get_current_facing(self) -> int:
        return self._current_facing
    
    def set_initial_offset(self, dir: int) -> None:
        self._initial_offset = dir

    def add_direction(self, dir: int) -> None:
        self._directions.append(dir)

    def next_direction(self) -> None:
        self._direction_index = (self._direction_index + 1) % len(self._directions)

    def prev_direction(self) -> None:
        self._direction_index = (self._direction_index - 1) % len(self._directions)

    def get_desired_direction(self) -> int:
        return self._directions[self._direction_index]
