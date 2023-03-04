import serial
import pybelt
import sys
import logging

from controller import Controller
from pybelt.belt_controller import BeltController, BeltMode, BeltConnectionState, BeltControllerDelegate, BeltVibrationTimerOption, BeltOrientationType

def interactive_belt_connection(belt_controller: BeltController) -> None:
	"""Procedures to connect a belt using the terminal.
	The procedure asks for the interface to use (serial port or Bluetooth) and connects the belt-controller using it.
	:param BeltController belt_controller: The belt-controller to connect.
	"""

	# List possible interfaces
	ports = serial.tools.list_ports.comports()
	if ports is None or len(ports) == 0:
		# Only Bluetooth available
		print("No serial port found (USB).")
		response = input("Connect the belt via Bluetooth? [y/n]")
		if response.lower() == "y":
			selected_interface = "Bluetooth"
		elif response.lower() == "n":
			return
		else:
			print("Unrecognized input.")
			return
	else:
		print(
			"Which interface do you want to use? [1-{}]".format(len(ports)+1))
		for i, port in enumerate(ports):
			print("{}. {}".format((i + 1), port[0]))
		print("{}. Bluetooth.".format(len(ports)+1))
		interface_number = input()
		try:
			interface_number_int = int(interface_number)
		except ValueError:
			print("Unrecognized input.")
			return
		if interface_number_int < 1 or interface_number_int > len(ports)+1:
			print("Unrecognized input.")
			return
		if interface_number_int == len(ports)+1:
			selected_interface = "Bluetooth"
		else:
			selected_interface = ports[interface_number_int-1][0]

	# Use serial port or Bluetooth to connect belt
	if selected_interface == "Bluetooth":
		# Bluetooth scan and connect
		with pybelt.belt_scanner.create() as scanner:
			print("Start BLE scan.")
			belts = scanner.scan()
			print("BLE scan completed.")
		if len(belts) == 0:
			print("No belt found.")
			return
		if len(belts) > 1:
			print("Select the belt to connect.")
			for i, belt in enumerate(belts):
				advertised_uuid = "Unknown"
				if 'uuids' in belt.metadata:
					for uuid in belt.metadata['uuids']:
						advertised_uuid = uuid
				print("{}. {} - {} - Adv. UUID {}".format((i + 1),
														  belt.name, belt.address, advertised_uuid))
			belt_selection = input("[1-{}]".format(len(belts)))
			try:
				belt_selection_int = int(belt_selection)
			except ValueError:
				print("Unrecognized input.")
				return
			print("Connect the belt.")
			belt_controller.connect(belts[belt_selection_int - 1])
		else:
			print("Connect the belt.")
			belt_controller.connect(belts[0])
	else:
		# Connect belt via serial port
		print("Connect the belt.")
		belt_controller.connect(selected_interface)


def belt_controller_log_to_stdout() -> None:
	"""Configures the belt-controller logger to print all debug messages on `stdout`.
	"""
	logger = pybelt.logger
	logger.setLevel(logging.DEBUG)
	sh = logging.StreamHandler(sys.stdout)
	sh_format = logging.Formatter(
		'\033[92m %(levelname)s: %(message)s \033[0m')
	sh.setFormatter(sh_format)
	sh.setLevel(logging.DEBUG)
	logger.addHandler(sh)

class Delegate(BeltControllerDelegate):
	_controller = None

	def __init__(self, controller: Controller):
		self._controller = controller

	def on_belt_button_pressed(self, button_id, previous_mode, new_mode):
		self._controller.belt_event_button_pressed(button_id, previous_mode, new_mode)

	def on_belt_orientation_notified(self, heading, is_orientation_accurate, extra):
		self._controller.belt_event_orientation_notified(heading, is_orientation_accurate, extra)

def connect_belt(controller: Controller) -> BeltController:
	belt_controller_log_to_stdout()

	belt_controller_delegate = Delegate(controller)
	belt_controller = BeltController(belt_controller_delegate)
	interactive_belt_connection(belt_controller)

	if belt_controller.get_connection_state() != BeltConnectionState.CONNECTED:
		return belt_controller

	# Change belt mode to APP mode
	belt_controller.set_belt_mode(BeltMode.APP_MODE)
	belt_controller.stop_vibration()

	return belt_controller
