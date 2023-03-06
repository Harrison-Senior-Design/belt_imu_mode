from serial.tools.list_ports import comports


def handle_input(controller, action):
    """
    Handle a keypress
    """
    if action == "c":
        controller.calibrate()
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
    """
    Get a key from the standard input
    """
    while controller.enabled:
        try:
            action = input()

            if not controller.enabled or not controller.is_connected():
                return None

            if len(action) == 0 or action is None:
                print("You must provide an input. Try again.")
            else:
                return action.lower()[0]
        except Exception as err:
            print(f"Caught exception handling input: {err}. Try again.")


def keyboard_thread(controller):
    """
    Entrypoint for thread listening for keyboard buttons
    """
    while controller.enabled:
        print("Q to quit.\nC to calibrate.\n")
        key = get_key(controller)

        if not controller.enabled:
            print("Shutting down")
            break
        elif not controller.is_connected():
            print(
                "Controller is disconnected -> wait for a re-connection before commands")
            continue

        try:
            handle_input(controller, key)
        except Exception as err:
            print(f"Caught exception handling action {key}: {err}")
