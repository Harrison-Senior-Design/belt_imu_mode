"""
Model for the program data
"""

from typing import Optional


class Model():
    """
    Holds all the relevant program data
    """
    _direction_index = 0
    _directions = []
    _controller = None
    _current_facing = 0
    _is_calibrated = False

    def set_current_facing(self, direction: int) -> None:
        """Set the current facing angle"""
        self._current_facing = direction

    def get_is_calibrated(self) -> bool:
        """Get the calibration stauts"""
        return self._is_calibrated

    def set_is_calibrated(self, calibrated: bool) -> None:
        """Set the calibration status"""
        self._is_calibrated = calibrated

    def get_current_facing(self) -> int:
        """Get current angle user is facing"""
        return self._current_facing

    def clear_directions(self) -> None:
        """Clear all directions"""
        self._directions.clear()
        self._direction_index = 0

    def get_direction_at(self, index: int) -> None:
        """Get direction at a given index"""
        return self._directions[index]

    def add_direction(self, direction: int) -> None:
        """Add a direction that we can point to"""
        self._directions.append(direction)

    def next_direction(self) -> None:
        """Cycle to next direction"""
        self._direction_index = (
            self._direction_index + 1) % len(self._directions)

    def prev_direction(self) -> None:
        """Cycle to prev direction"""
        self._direction_index = (
            self._direction_index - 1) % len(self._directions)

    def get_desired_direction(self) -> Optional[int]:
        """Get desired direction we want to point at"""
        if len(self._directions) <= self._direction_index:
            return None

        return self._directions[self._direction_index]
