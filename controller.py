import threading
from model import Model
from util.belt_util import disconnect_belt
from pybelt.belt_controller import BeltMode, BeltController, BeltConnectionState

class Controller():
    _lock = threading.Lock()
    _belt_controller = None
    
    views = []
    model = None

    def __init__(self):
        self.model = Model(self)

    def set_belt_controller(self, belt_controller: BeltController) -> None:
        self._belt_controller = belt_controller

    def get_belt_controller(self) -> BeltController:
        return self._belt_controller

    def add_view(self, view) -> None:
        self.views.append(view)

    def cleanup(self) -> None:
        disconnect_belt(self._belt_controller)

    def is_connected(self) -> bool:
        return self._belt_controller.get_connection_state() == BeltConnectionState.CONNECTED

    def calibrate(self) -> None:
        self.model.set_initial_offset(self.model.get_current_facing())

    def vibrate_at_with_offset(self, dir: int, channel = 1) -> None:
        final_angle = self.model.get_desired_direction() - self.model.get_desired_direction()
        final_angle = final_angle % 360

        self._belt_controller.vibrate_at_angle(final_angle, channel_index=channel)

    def belt_event_button_pressed(self, button_id, previous_mode, new_mode) -> None:
        with self._lock:
            if new_mode != BeltMode.APP_MODE:
                self._belt_controller.set_belt_mode(BeltMode.APP_MODE)

    def belt_event_orientation_notified(self, heading, is_orientation_accurate, extra) -> None:
        with self._lock:
            self.model.set_current_facing(heading)

            self.vibrate_at_with_offset(self.model.get_desired_direction())
