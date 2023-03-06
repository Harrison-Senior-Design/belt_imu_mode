from model import Model
from views.view import View

from screen_library.lcd.lcd_comm import Orientation
from screen_library.lcd.lcd_comm_rev_b import LcdCommRevB

from datetime import datetime

import math

class USBView(View):
    _lcd_comm = None

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
    
    def clean_screen(self):
        self._lcd_comm.Clear()

    def cleanup(self):
        self._lcd_comm.closeSerial()

    def get_display_coords(self, heading: 0, radius, center):
        rad = math.radians(heading)
        x = math.cos(rad)
        y = math.sin(rad)
        x = int(x*radius + center[0])
        y = int(y*radius + center[1])
        return x,y

    def clear_prev(self, prev_heading):
        heading = prev_heading
        new_heading = heading - 90
        x,y = self.get_display_coords(new_heading, 100, [150,300])
        self._lcd_comm.DisplayText("_", x, y,
                                   font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
                                   font_size=50,
                                   font_color=(255, 0, 0))
        
        x,y = self.get_display_coords(new_heading+90, 100, [150,300])
        self._lcd_comm.DisplayText("_", x, y,
                                   font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
                                   font_size=50,
                                   font_color=(255, 0, 0))
        
        x,y = self.get_display_coords(new_heading+180, 100, [150,300])
        self._lcd_comm.DisplayText("_", x, y,
                                   font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
                                   font_size=50,
                                   font_color=(255, 0, 0))
        
        x,y = self.get_display_coords(new_heading+270, 100, [150,300])
        self._lcd_comm.DisplayText("_", x, y,
                                   font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
                                   font_size=50,
                                   font_color=(255, 0, 0))

    def render(self, prev_heading, heading):
        # self.clean_screen()
        self.clear_prev(prev_heading)
        # implementation for rendering on the USB screen
        background = "C:/Users/abhig/Documents/GitHub/Harrison-Senior-Design/belt_imu_mode/assets/example_landscape.png"

        # Status
        self._lcd_comm.DisplayText("Status: Connected", 4, 4,
                                   font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
                                   font_size=12,
                                   font_color=(255, 0, 0))
        
        # # Facing Wall
        # self._lcd_comm.DisplayText("Facing Wall:", 180, 4,
        #                            font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
        #                            font_size=15,
        #                            font_color=(255, 0, 0))
        # self._lcd_comm.DisplayText("A", 260, 40,
        #                            font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
        #                            font_size=40,
        #                            font_color=(255, 0, 0))

        ### Compass Display   radius = 100, center = 150, 300
        new_heading = heading - 90
        x,y = self.get_display_coords(new_heading, 100, [150,300])
        self._lcd_comm.DisplayText("A", x, y,
                                   font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
                                   font_size=50,
                                   font_color=(255, 0, 0))
        
        x,y = self.get_display_coords(new_heading+90, 100, [150,300])
        self._lcd_comm.DisplayText("B", x, y,
                                   font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
                                   font_size=50,
                                   font_color=(255, 0, 0))
        
        x,y = self.get_display_coords(new_heading+180, 100, [150,300])
        self._lcd_comm.DisplayText("C", x, y,
                                   font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
                                   font_size=50,
                                   font_color=(255, 0, 0))
        
        x,y = self.get_display_coords(new_heading+270, 100, [150,300])
        self._lcd_comm.DisplayText("D", x, y,
                                   font="./assets/fonts/roboto-mono/RobotoMono-Regular.ttf",
                                   font_size=50,
                                   font_color=(255, 0, 0))

    def update(self):
        # implementation for updating the USB screen
        pass
