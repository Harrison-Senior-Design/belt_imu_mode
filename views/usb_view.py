"""
Module for controlling the USB screen view
"""

import math

from PIL import Image

from model import Model
from views.view import View

from screen_library.lcd.lcd_comm import Orientation
from screen_library.lcd.lcd_comm_rev_b import LcdCommRevB


class USBView(View):
    """
    View class representing a USB screen plugged in
    """
    _lcd_comm = None

    prev_rotation = None
    prev_connection_text = None

    _font_path = "./assets/fonts/roboto-mono/RobotoMono-Regular.ttf"

    compass_radius = 100
    compass_origin_x = 150
    compass_origin_y = 300

    def __init__(self, controller):
        super().__init__(controller)
        self._lcd_comm = LcdCommRevB(com_port="COM4",
                                     display_width=320,
                                     display_height=480)

        self._lcd_comm.Reset()
        self._lcd_comm.InitializeComm()
        self._lcd_comm.SetBrightness(level=30)
        self._lcd_comm.SetOrientation(orientation=Orientation.PORTRAIT)
        self._lcd_comm.SetBackplateLedColor(led_color=(255, 255, 255))

        self.clear_screen()

    def clear_screen(self):
        """
        Reset the screen
        The implementation of this is very slow -> clears pixels line by line
        Should be avoided
        """
        self._lcd_comm.Clear()

    def cleanup(self):
        self.clear_screen()
        self._lcd_comm.closeSerial()

    def get_compass_coords(self, heading, radius, center_x, center_y):
        """
        Get x and y coordinates
        of where a specific heading should be on the compass
        """

        rad = math.radians(heading)
        x_coord = math.cos(rad)
        y_coord = math.sin(rad)

        x_coord = int(x_coord * radius) + center_x
        y_coord = int(y_coord * radius) + center_y

        return x_coord, y_coord

    def clear_prev_compass(self, rotation_amount: int):
        """
        Render the compass
        """

        a_x, a_y = self.get_compass_coords(heading=rotation_amount,
                                           center_x=self.compass_origin_x,
                                           center_y=self.compass_origin_y,
                                           radius=self.compass_radius)

        b_x, b_y = self.get_compass_coords(heading=rotation_amount + 90,
                                           center_x=self.compass_origin_x,
                                           center_y=self.compass_origin_y,
                                           radius=self.compass_radius)

        c_x, c_y = self.get_compass_coords(heading=rotation_amount + 180,
                                           center_x=self.compass_origin_x,
                                           center_y=self.compass_origin_y,
                                           radius=self.compass_radius)

        d_x, d_y = self.get_compass_coords(heading=rotation_amount + 270,
                                           center_x=self.compass_origin_x,
                                           center_y=self.compass_origin_y,
                                           radius=self.compass_radius)

        background = Image.new(
            'RGB',
            (50, 50),
            (255, 255, 255)
        )

        self._lcd_comm.DisplayPILImage(background, x=a_x, y=a_y)
        self._lcd_comm.DisplayPILImage(background, x=b_x, y=b_y)
        self._lcd_comm.DisplayPILImage(background, x=c_x, y=c_y)
        self._lcd_comm.DisplayPILImage(background, x=d_x, y=d_y)

    def render_status_text(self, is_connected: bool):
        """Render text displaying belt connection status"""
        connection_string = "Connected" if is_connected else "Disconnected"
        text = f"Status: {connection_string}"

        if text == self.prev_connection_text:
            # don't re-render if there are no updates
            return

        # Clear previous text bounding box
        background = Image.new(
            'RGB',
            (140, 12),
            (255, 255, 255)
        )

        self._lcd_comm.DisplayPILImage(background, x=4, y=4)

        # Write text again
        self._lcd_comm.DisplayText(text,
                                   x=4,
                                   y=4,
                                   font=self._font_path,
                                   font_size=12,
                                   font_color=(255, 0, 0))

        self.prev_connection_text = text

    def render_compass(self, rotation_amount: int):
        """
        Render the compass
        """

        a_x, a_y = self.get_compass_coords(heading=rotation_amount,
                                           center_x=self.compass_origin_x,
                                           center_y=self.compass_origin_y,
                                           radius=self.compass_radius)

        b_x, b_y = self.get_compass_coords(heading=rotation_amount + 90,
                                           center_x=self.compass_origin_x,
                                           center_y=self.compass_origin_y,
                                           radius=self.compass_radius)

        c_x, c_y = self.get_compass_coords(heading=rotation_amount + 180,
                                           center_x=self.compass_origin_x,
                                           center_y=self.compass_origin_y,
                                           radius=self.compass_radius)

        d_x, d_y = self.get_compass_coords(heading=rotation_amount + 270,
                                           center_x=self.compass_origin_x,
                                           center_y=self.compass_origin_y,
                                           radius=self.compass_radius)

        self._lcd_comm.DisplayText("A", a_x, a_y,
                                   font=self._font_path,
                                   font_size=50,
                                   font_color=(255, 0, 0))

        self._lcd_comm.DisplayText("B", b_x, b_y,
                                   font=self._font_path,
                                   font_size=50,
                                   font_color=(255, 0, 0))

        self._lcd_comm.DisplayText("C", c_x, c_y,
                                   font=self._font_path,
                                   font_size=50,
                                   font_color=(255, 0, 0))

        self._lcd_comm.DisplayText("D", d_x, d_y,
                                   font=self._font_path,
                                   font_size=50,
                                   font_color=(255, 0, 0))

    def render(self, model: Model):
        is_connected = self._controller.is_connected()
        self.render_status_text(is_connected)

        if is_connected and model.get_is_calibrated():
            facing = model.get_current_facing()
            rotation_amount = (facing - model.get_direction_at(0) - 90) % 360

            if rotation_amount == self.prev_rotation:
                # don't re-render if there are no updates
                return

            if self.prev_rotation is not None:
                self.clear_prev_compass(self.prev_rotation)
            self.prev_rotation = rotation_amount

            self.render_compass(rotation_amount)

        # # Facing Wall
        # self._lcd_comm.DisplayText("Facing Wall:", 180, 4,
        #                            font=self._font_path,
        #                            font_size=15,
        #                            font_color=(255, 0, 0))
        # self._lcd_comm.DisplayText("A", 260, 40,
        #                            font=self._font_path,
        #                            font_size=40,
        #                            font_color=(255, 0, 0)
