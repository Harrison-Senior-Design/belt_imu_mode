from util.belt_util import connect_belt
from controller import Controller
from views.usb_view import USBView

from serial.tools.list_ports import comports

import threading


def handle_input(controller, action):
    action = action.lower()

    if action == "c":
        controller.calibrate()
    elif action == "r":
        print("Rendering all views")

        controller.render_views()
    elif action == "q":
        print("Quitting program")
        controller.cleanup()
    elif action == "p":
        com_ports = comports()

        for com_port in com_ports:
            print(f"Port: {com_port.__dict__}")
    else:
        print("Unrecognized input.")


def get_key(controller):
    while controller.is_connected():
        try:
            action = input()

            if len(action) == 0:
                print(f"You must provide an input. Try again.")
            else:
                return action.lower()[0]
        except Exception as err:
            print(f"Caught exception handling input: {err}. Try again.")


def keyboard_thread(controller):
    while controller.is_connected():
        print("Q to quit.\nC to calibrate.\n")
        key = get_key(controller)

        try:
            handle_input(controller, key)
        except Exception as err:
            print(f"Caught exception handling action {key}: {err}")


def main():
    controller = Controller()

    belt_controller = connect_belt(controller)
    controller.set_belt_controller(belt_controller)

    # usb_screen_view = USBView(controller)

    # controller.add_view(usb_screen_view)

    kb_thread = threading.Thread(target=keyboard_thread, args=(controller,))
    kb_thread.start()
    kb_thread.join()


if __name__ == '__main__':
    main()
