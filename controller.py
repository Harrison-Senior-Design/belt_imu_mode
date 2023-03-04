import threading
from model import Model
from pybelt.belt_controller import BeltMode, BeltController, BeltConnectionState
from constants import VIBRATION_INTENSITY, ButtonIDs

from views.view import View


class Controller():
    _lock = threading.Lock()
    _belt_controller = None

    views = []
    model = None

    def __init__(self):
        self.model = Model()

    def set_belt_controller(self, belt_controller: BeltController) -> None:
        self._belt_controller = belt_controller

    def get_belt_controller(self) -> BeltController:
        return self._belt_controller

    def add_view(self, view: View) -> None:
        self.views.append(view)

    def cleanup(self) -> None:
        for view in self.views:
            view.cleanup()
        self.views.clear()

        self._belt_controller.stop_vibration()
        self._belt_controller.set_belt_mode(BeltMode.PAUSE)
        self._belt_controller.disconnect_belt()

    def is_connected(self) -> bool:
        return self._belt_controller.get_connection_state() == BeltConnectionState.CONNECTED

    def calibrate(self) -> None:
        with self._lock:
            wall_a = (self.model.get_current_facing() - 180) % 360
            wall_b = (wall_a + 90) % 360
            wall_c = (wall_b + 90) % 360
            wall_d = (wall_c + 90) % 360

            self.model.clear_directions()
            self.model.add_direction(wall_a)
            self.model.add_direction(wall_b)
            self.model.add_direction(wall_c)
            self.model.add_direction(wall_d)

            self.model.set_is_calibrated(True)

            print(f"Facing {self.model.get_current_facing()}")
            print(f"Calibrated for wall A to be at angle {wall_a}")

    def vibrate_at_with_offset(self, dir_to_vibrate: int, channel=0) -> None:
        if not self.model.get_is_calibrated():
            return

        offset_dist_from_zero = 360 - dir_to_vibrate
        cur_dist_from_zero = 360 - self.model.get_current_facing()

        final_angle = cur_dist_from_zero - offset_dist_from_zero
        final_angle = final_angle % 360
        print(f"Vibrate at final angle {final_angle} (post-offset)")

        self._belt_controller.vibrate_at_angle(
            final_angle,
            channel_index=channel,
            intensity=VIBRATION_INTENSITY,
            switch_to_app_mode=True)

    def belt_event_button_pressed(
            self,
            button_id,
            previous_mode,
            new_mode) -> None:
        if new_mode != BeltMode.APP_MODE:
            print(f"back to app mode!!")
            self._belt_controller.set_belt_mode(BeltMode.APP_MODE)

        if button_id == ButtonIDs.COMPASS.value:
            print(f"Pressed COMPASS, re-calibrating")
            self.calibrate()
        elif button_id == ButtonIDs.PAUSE.value:
            print(f"Pressed PAUSE, cycling to prev direction")
            self.prev_direction()
        elif button_id == ButtonIDs.HOME.value:
            print(f"Pressed HOME, cycling to next direction")
            self.next_direction()

    def next_direction(self):
        with self._lock:
            self.model.next_direction()

    def prev_direction(self):
        with self._lock:
            self.model.prev_direction()

    def belt_event_orientation_notified(
            self,
            heading,
            is_orientation_accurate,
            extra) -> None:
        with self._lock:
            self.model.set_current_facing(heading)

            desired_direction = self.model.get_desired_direction()
            if desired_direction is not None:
                self.vibrate_at_with_offset(desired_direction)

    def render_views(self) -> None:
        for view in self.views:
            view.render(self.model)
