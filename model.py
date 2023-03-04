from typing import Optional


class Model():
    _direction_index = 0
    _directions = []
    _controller = None
    _current_facing = 0
    _is_calibrated = False

    def set_current_facing(self, dir: int) -> None:
        self._current_facing = dir

    def get_is_calibrated(self) -> bool:
        return self._is_calibrated
    
    def set_is_calibrated(self, calibrated: bool) -> None:
        self._is_calibrated = calibrated

    def get_current_facing(self) -> int:
        return self._current_facing

    def clear_directions(self) -> None:
        self._directions.clear()
        self._direction_index = 0

    def add_direction(self, dir: int) -> None:
        self._directions.append(dir)

    def next_direction(self) -> None:
        self._direction_index = (self._direction_index + 1) % len(self._directions)

    def prev_direction(self) -> None:
        self._direction_index = (self._direction_index - 1) % len(self._directions)

    def get_desired_direction(self) -> Optional[int]:
        if len(self._directions) <= self._direction_index:
            return None
        
        return self._directions[self._direction_index]
