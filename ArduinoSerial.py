#!/usr/bin/env python

import logging
from serial import Serial, SerialException
from time import sleep


class ArduinoSerial(object):
    
    DEFAULT_BAUD = 115200
    _logger = logging.getLogger("ArduinoSerial")

    def __init__(self, port, scalex=1, scaley=1):
        self._serial = Serial()
        self._scale_x = scalex
        self._scale_y = scaley
        self.open(port)

    def _send_gcode(self, gcode):
        if gcode:
            self._logger.debug("sending gcode %s", gcode)
        #gcode += "\n"
        try:
            self._serial.write("%s\r\n" % (gcode,))
            # Wait for grbl response with carriage return
            grbl_out = self._serial.readline().strip()
        except SerialException:
            pass
        else:
            if grbl_out:
                self._logger.debug("recived %s", grbl_out)

    def _go_to(self, point):
        """
        Send a command to the arduino to move the magnet to a specific (x, y)
        """
        self._logger.debug("going to %s", point)
        self._send_gcode("G90X%sY%s" % (point[1] * self._scale_y, point[0] * self._scale_x))

    def _set_magnet_state(self, is_on):
        """
        Send a command to the arduino to activate/deactivate the magnet
        """
        self._logger.debug("turning magnet %s", "on" if is_on else "off")
        self._send_gcode("M4" if is_on else "M3")

    def open(self, port, baud=DEFAULT_BAUD):
        try:
            self._serial = Serial(port=port, baudrate=baud)
            self._serial.open()
        except Exception as e:
            self._logger.error('Failed to open {}'.format(e))
	    return
        self._send_gcode("")
        self._send_gcode("")
        self._logger.info("%s is opened", self._serial.port)

    def close(self):
        self._serial.close()
        self._logger.info("%s is closed", self._serial.port)

    def move(self, points):
        """
        Move a game piece via the given points
        """
        self._logger.info("moving via %s", points)
        # deactivate the magnet for safety before moving
        self._set_magnet_state(False)
        # go to the 'from' piece location
        self._go_to(points.pop(0))
        # activate the magnet for moving
        self._set_magnet_state(True)
        # move via the points (dragging the piece with the magnet)
        for point in points:
            self._go_to(point)
        # deactivate the magnet for safety
        self._set_magnet_state(False)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s:\n%(message)s",
        datefmt="%d/%m/%y %H:%M:%S",
        level=logging.DEBUG)
    from IPython.terminal.embed import InteractiveShellEmbed
    globals().update(locals())
    arduino_serial = ArduinoSerial("/dev/ttyUSB0")
    InteractiveShellEmbed(banner1="", confirm_exit=False, exit_msg="Bye :)")()
    arduino_serial.close()

