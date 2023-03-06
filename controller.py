import threading
from model import Model
from pybelt.belt_controller import BeltMode, BeltController, BeltConnectionState
from constants import VIBRATION_INTENSITY, ButtonIDs

from views.view import View
from util.belt_util import auto_belt_connection


class Controller():
    """
    Controller for the whole program.
    Handles belt events, talks to the model, tells views when to render
    """
    _lock = threading.Lock()
    _belt_controller = None

    enabled = True

    views = []
    model = None

    def __init__(self):
        self.model = Model()

    def set_belt_controller(self, belt_controller: BeltController) -> None:
        """Set the belt controller"""
        self._belt_controller = belt_controller

    def get_belt_controller(self) -> BeltController:
        """Get the belt controller"""
        return self._belt_controller

    def add_view(self, view: View) -> None:
        """
        Add a view to re-render when the controller gets updates
        """
        self.views.append(view)

    def cleanup(self) -> None:
        """
        Cleanup resources before shutting down
        """
        for view in self.views:
            view.cleanup()
        self.views.clear()

        self.enabled = False

        if self.is_connected():
            self._belt_controller.stop_vibration()
            self._belt_controller.set_belt_mode(BeltMode.PAUSE)
            self._belt_controller.disconnect_belt()

    def is_connected(self) -> bool:
        """
        Check if the belt is connected
        """
        return self._belt_controller.get_connection_state() == BeltConnectionState.CONNECTED

    def reconnect(self):
        """
        Auto-reconnect the belt by scanning available ports
        """
        return auto_belt_connection(self, self._belt_controller)

    def calibrate(self) -> None:
        """
        Calibrate the belt.
        This sets wall A to behind the current facing,
        calculates the other 3 walls,
        and clears the previous set directions.
        """
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
        """
        Vibrate the belt calculating the necessary offset
        based on where the belt currently is facing
        """
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
        """
        Event that gets triggered when a button is
        pressed on the belt.
        """

        if new_mode != BeltMode.APP_MODE:
            self._belt_controller.set_belt_mode(BeltMode.APP_MODE)

        if button_id == ButtonIDs.COMPASS.value:
            print("Pressed COMPASS, re-calibrating")
            self.calibrate()
        elif button_id == ButtonIDs.PAUSE.value:
            print("Pressed PAUSE, cycling to prev direction")
            self.prev_direction()
        elif button_id == ButtonIDs.HOME.value:
            print("Pressed HOME, cycling to next direction")
            self.next_direction()

    def next_direction(self):
        """
        Cycle the belt to point in the next available direction
        """
        with self._lock:
            self.model.next_direction()

    def prev_direction(self):
        """
        Cycle the belt to point in the previous available direction
        """
        with self._lock:
            self.model.prev_direction()

    def belt_event_orientation_notified(
            self,
            heading,
            is_orientation_accurate,
            extra) -> None:
        """
        Event called when the belt IMU notifies
        us of a new orientation
        """
        with self._lock:
            self.model.set_current_facing(heading)

            desired_direction = self.model.get_desired_direction()
            if desired_direction is not None:
                self.vibrate_at_with_offset(desired_direction)

    def render_views(self) -> None:
        """
        Render all views
        """
        if not self.enabled:
            return

        for view in self.views:
            view.render(self.model)
