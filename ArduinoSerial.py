class ArduinoSerial(object):
	def __init__(self):
		"""
		Initialize the communication with the arduino
		"""
		print '[ArduinoSerial] instance initiallized'

	def _go_to(self, x, y):
		"""
		Send a command to the arduino to move the magnet to a specific (x, y)
		"""
		print '[ArduinoSerial] ordered the arduino to move the magnet to ({},{})'.format(x, y)

	def _set_magnet_state(self, on):
		"""
		Send a command to the arduino to activate/deactivate the magnet
		"""
		print '[ArduinoSerial] setting magnet state to {}'.format('on' if on else 'off')

	def move(self, x_from, y_from, x_to, y_to):
		"""
		Move a game piece from (x_from, y_from) to (x_to, y_to)
		"""
		# deactivate the magnet for safety before moving
		self._set_magnet_state(False)

		# go to the 'from' piece location
		self._go_to(x_from, y_from)

		# activate the magnet for moving
		self._set_magnet_state(True)
		
		# go to the 'to' location (dragging the piece with us using the magnet)
		self._go_to(y_to, y_to)

		# deactivate the magnet for safety
		self._set_magnet_state(False)