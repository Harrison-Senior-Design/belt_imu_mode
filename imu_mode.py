import sys
import math
import traceback
import keyboard
from pynput.keyboard import Key, Listener
import msvcrt

# from python_socket_sdk.core.socket import Socket
from belt import connect_belt, disconnect_belt, get_heading

from pybelt.belt_controller import BeltConnectionState, BeltVibrationPattern, BeltOrientationType

######################################################################################################
# We want the belt to read from an external imu to get data for where to vibrate.
# We will adjust certain things about the belt using keyboard input
# The proof of concept will be done with the belt's own imu, then an external imu will be integrated
# Required functionality:
#   - Button to reset vibration pointer to in front
#   - Buttons to set vibration pointer to the right, left, front, back
######################################################################################################

# class ImuMode:
#     def __init__(self, controller):
#         self._left = 0
#         self._right = 0
#         self._front = 0
#         self._back = 0
#         self._setpoint = 0
#         self._belt = controller

#     def calibrate(self, heading):
#         self._setpoint = heading
#         self._front = (self._setpoint) % 360
#         self._right = (self._setpoint + 90) % 360
#         self._left = (self._setpoint + 270) % 360
#         self._back = (self._setpoint + 180) % 360
    
#     def vibrate_at_ang(self, ang=None):
#         if ang == None:
#             ang = self._setpoint
#         self._belt.vibrate_at_angle(ang, channel_index=0)
    
#     def vibrate_at_compass(self, dir):
#         self._belt.vibrate_at_magnetic_bearing(dir, channel_index=1)
    
#     def handle_input(self, inp):
#         if (inp in ['w','a','s','d']):
#             if (inp == 'w'):
#                 self._setpoint = self._front
#             elif (inp == 'a'):
#                 self._setpoint = self._right
#             elif (inp == 's'):
#                 self._setpoint = self._back
#             elif (inp == 'd'):
#                 self._setpoint = self._left
#             self.vibrate_at_ang()
#         elif inp in ['up','down','left','right']:
#             if (inp == 'up'):
#                 dir = 0
#             elif (inp == 'left'):
#                 dir = 90
#             elif (inp == 'down'):
#                 dir = 180
#             elif (inp == 'right'):
#                 dir = 270
#             self.vibrate_at_compass(dir)
#         else:
#             self.vibrate_at_ang(self._setpoint-self._belt._heading_offset)

# def main2():
#     belt_controller = connect_belt()
#     belt = ImuMode(belt_controller)
#     belt.calibrate(belt_controller._heading_offset)

#     while belt_controller.get_connection_state() == BeltConnectionState.CONNECTED:
#         belt.vibrate_at_ang()
#         inp = keyboard.read_key()
#         if inp == 'q':
#             disconnect_belt(belt_controller)
#             break
#         belt.handle_input(inp)


belt_controller = connect_belt()

def vibrate_at(mode, ang):
    if mode == "ang":
        belt_controller.vibrate_at_angle(ang, channel_index=0)
    else:
        belt_controller.vibrate_at_magnetic_bearing(ang, channel_index=1)

# def change_setpoint(inp, setpoint):
#     if (inp == 'c'):
#         new_setpoint = belt_controller._heading_offset
#         vibrate_at(setpoint)
#         return new_setpoint
    
#     # Vibrate at Front, Left, Back, Right relative to where user is facing
#     if (inp == 'w'):
#         vibrate_at("ang",setpoint)
#     elif (inp == 'a'):
#         vibrate_at("ang",(setpoint+90)%360)
#     elif (inp == 's'):
#         vibrate_at("ang",(setpoint+180)%360)
#     elif (inp == 'd'):
#         vibrate_at("ang",(setpoint+270)%360)
    
#     # Vibrate at true North, East, South, West
#     elif (inp == 'i'):
#         vibrate_at("compass",0)
#     elif (inp == 'j'):
#         vibrate_at("compass",90)
#     elif (inp == 'k'):
#         vibrate_at("compass",180)
#     elif (inp == 'l'):
#         vibrate_at("compass",270)
    
#     return setpoint

# def main():
#     if belt_controller.get_connection_state() != BeltConnectionState.CONNECTED:
#         print("Belt connection failed")
#         return 0
    
#     setpoint = belt_controller._heading_offset
#     vibrate_at("ang",setpoint)

#     while belt_controller.get_connection_state() == BeltConnectionState.CONNECTED:
#         # with Listener(on_release=on_release) as listener:
#         #     listener.join()
#         print(f"Heading: {belt_controller._heading_offset}")
#         inp = keyboard.read_key()
#         if (inp == 'q'):
#             disconnect_belt(belt_controller)
#             break
#         elif inp is not None:
#             setpoint = change_setpoint(inp, setpoint)
#         else:
#             vibrate_at("ang", setpoint+(setpoint-belt_controller._heading_offset))


setpoint = get_heading()
front = (setpoint) % 360
right = (setpoint + 90) % 360
left = (setpoint + 270) % 360
back = (setpoint + 180) % 360

def on_release(key):
    if (key == 'q'):
        disconnect_belt(belt_controller)
        return False
    elif (key in ['w','a','s','d']):
        if (key == 'w'):
            setpoint = front
        elif (key == 'a'):
            setpoint = right
        elif (key == 's'):
            setpoint = back
        elif (key == 'd'):
            setpoint = left
        mode = "ang"
        vibrate_at(mode, setpoint)
    elif key in ['up','down','left','right']:
        if (key == 'up'):
            dir = 0
        elif (key == 'left'):
            dir = 90
        elif (key == 'down'):
            dir = 180
        elif (key == 'right'):
            dir = 270
        mode = "compass"
        vibrate_at(mode, dir)
    else:
        pass
        vibrate_at(mode, setpoint-belt_controller._heading_offset)

def calibrate():
    print("Calibrate setpoint 1: Hit enter to continue")
    _set = None
    while _set is None:
        if keyboard.read_key() == "enter":
            _set = get_heading()
    return _set

def main3():

    if belt_controller.get_connection_state() != BeltConnectionState.CONNECTED:
        print("Belt connection failed")
        return 0
    
    setpoint = calibrate()
    front = (setpoint) % 360
    right = (setpoint + 90) % 360
    left = (setpoint + 270) % 360
    back = (setpoint + 180) % 360
    print("Ready to run")
    mode = "ang"
    belt_controller.vibrate_at_angle((get_heading()-setpoint)%360, channel_index=0)
    while belt_controller.get_connection_state() == BeltConnectionState.CONNECTED:
        # with Listener(on_release=on_release) as listener:
        #     listener.join()
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            if (inp == 'q'):
                disconnect_belt(belt_controller)
                break
            if (inp in ['w','a','s','d']):
                if (inp == 'w'):
                    setpoint = front
                elif (inp == 'a'):
                    setpoint = right
                elif (inp == 's'):
                    setpoint = back
                elif (inp == 'd'):
                    setpoint = left
                mode = "ang"
        belt_controller.vibrate_at_angle((get_heading()-setpoint)%360, channel_index=0)
        print((get_heading()-setpoint)%360)
        # print("hi")
        # print(f"Heading: {belt_controller._delegate}")
        # belt_controller._delegate.on_belt_orientation_notified()
        # else:
        #     pass

# def main4():
#     if belt_controller.get_connection_state() != BeltConnectionState.CONNECTED:
#         print("Belt connection failed")
#         return 0
    
#     setpoint = 50
#     while belt_controller.get_connection_state() == BeltConnectionState.CONNECTED:
#         print(get_heading())
#         vibrate_at("ang", (setpoint-get_heading())%360)
#         if msvcrt.kbhit():
#             inp = msvcrt.getch()
#             if (inp == 'q'):
#                 disconnect_belt(belt_controller)
#                 break


if __name__ == '__main__':
    try:
        main3()
    except Exception as e:
        print('Got an exception -> forcing shut-down')

        traceback.print_exc()