import threading

from time import sleep

from controller import Controller
from util.belt_util import init_belt
from view_thread import view_thread_entrypoint
from views.usb_view import USBView
from keyboard_input import keyboard_thread


def main():
    """
    Main function of entire program
    """
    controller = Controller()

    belt_controller = init_belt(controller)
    controller.set_belt_controller(belt_controller)

    usb_screen_view = USBView(controller)

    controller.add_view(usb_screen_view)

    kb_thread = threading.Thread(target=keyboard_thread, args=(controller,))
    kb_thread.start()

    view_thread = threading.Thread(
        target=view_thread_entrypoint, args=(controller,))
    view_thread.start()

    while controller.enabled:
        if not controller.is_connected() and controller.enabled:
            controller.reconnect()

        sleep(1)

    # join threads after controlled is "disabled"
    view_thread.join()
    kb_thread.join()


if __name__ == '__main__':
    main()
