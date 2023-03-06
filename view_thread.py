"""Thread for views to keep re-rendering"""

from time import sleep

from controller import Controller

FPS = 3
SLEEP_TIME = 1 / FPS  # 1 second divided by desired FPS


def view_thread_entrypoint(controller: Controller):
    """Entrypoint for view thread"""
    while controller.enabled:
        controller.render_views()

        sleep(1 / FPS)
