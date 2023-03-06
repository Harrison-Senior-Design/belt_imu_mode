import threading

from time import sleep

from controller import Controller
from util.belt_util import init_belt
from views.usb_view import USBView
from keyboard_input import keyboard_thread


def main():
    controller = Controller()

    belt_controller = init_belt(controller)
    controller.set_belt_controller(belt_controller)

    usb_screen_view = USBView(controller)

    controller.add_view(usb_screen_view)

    prev_heading = 0
    for heading in range(0, 90):
        usb_screen_view.render(prev_heading, heading)
        prev_heading = heading

    kb_thread = threading.Thread(target=keyboard_thread, args=(controller,))
    kb_thread.start()

    while controller.enabled:
        if not controller.is_connected() and controller.enabled:
            controller.reconnect()

        sleep(1)

    # join thread after controlled is "disabled"
    kb_thread.join()


if __name__ == '__main__':
    main()
