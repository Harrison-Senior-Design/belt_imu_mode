import time

from util.belt_util import connect_belt
from controller import Controller
from views.view import View

def main():
    controller = Controller()

    belt_controller = connect_belt(controller)
    controller.set_belt_controller(belt_controller)

    gui_view = View(controller)

    controller.add_view(gui_view)

    while controller.is_connected():
        print("Q to quit.")
        action = input()

        if action.lower() == "q" or action.lower() == "quit":
            print("Quitting program")

            break
        else:
            print("Unrecognized input.")

    controller.cleanup()

if __name__ == '__main__':
    main()
