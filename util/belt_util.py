import serial
import pybelt
import sys
import logging
import constants

from time import sleep
from pybelt.belt_controller import BeltController, BeltMode, BeltConnectionState, BeltControllerDelegate, BeltVibrationTimerOption, BeltOrientationType


def find_belt_comport():
    ports = serial.tools.list_ports.comports()

    if ports is None or len(ports) == 0:
        return None

    for port in ports:
        if port.serial_number == constants.BELT_SERIAL_NUMBER:
            return port

    return None


def auto_belt_connection(controller, belt_controller: BeltController) -> None:
    port = None

    print("Attemping auto connection... scanning ports")

    while port is None and controller.enabled:
        port = find_belt_comport()

        if port is None:
            print("Belt device not found. Make sure it is plugged in and turned on!")
            print("Trying again in 5 seconds.")

            sleep(5)

    if not controller.enabled:
        print("Shutting down...")

    print(f"Connecting to port {port.name}")
    belt_controller.connect(port.name)

    belt_controller.set_belt_mode(BeltMode.APP_MODE)
    belt_controller.stop_vibration()


def belt_controller_log_to_stdout() -> None:
    """Configures the belt-controller logger to print all debug messages on `stdout`.
    """
    logger = pybelt.logger
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    sh_format = logging.Formatter(
        '\033[92m %(levelname)s: %(message)s \033[0m')
    sh.setFormatter(sh_format)
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)


class Delegate(BeltControllerDelegate):
    _controller = None

    def __init__(self, controller):
        self._controller = controller

    def on_belt_button_pressed(self, button_id, previous_mode, new_mode):
        self._controller.belt_event_button_pressed(
            button_id, previous_mode, new_mode)

    def on_belt_orientation_notified(self, heading, is_orientation_accurate, extra):
        self._controller.belt_event_orientation_notified(
            heading, is_orientation_accurate, extra)


def init_belt(controller) -> BeltController:
    # belt_controller_log_to_stdout()

    belt_controller_delegate = Delegate(controller)
    belt_controller = BeltController(belt_controller_delegate)

    return belt_controller
