from model import Model
from views.view import View

from screen_library.lcd.lcd_comm import Orientation
from screen_library.lcd.lcd_comm_rev_b import LcdCommRevB

from datetime import datetime

class USBView(View):
    _lcd_comm = None

    def __init__(self, controller):
        super().__init__(controller)
        self._lcd_comm = LcdCommRevB(com_port="COM4",
                                     display_width=320,
                                     display_height=480)

        self._lcd_comm.Reset()
        self._lcd_comm.InitializeComm()
        self._lcd_comm.SetBrightness(level=50)
        self._lcd_comm.SetOrientation(orientation=Orientation.PORTRAIT)
        self._lcd_comm.SetBackplateLedColor(led_color=(255, 255, 255))

    def cleanup(self):
        self._lcd_comm.closeSerial()

    def render(self, model: Model):
        # implementation for rendering on the USB screen
        background = "assets/example_landscape.png"
        self._lcd_comm.DisplayText(str(datetime.now().time()), 160, 2,
                                   font="assets/RobotoMono-Medium.ttf",
                                   font_size=20,
                                   font_color=(255, 0, 0),
                                   background_image=background)

    def update(self):
        # implementation for updating the USB screen
        pass
