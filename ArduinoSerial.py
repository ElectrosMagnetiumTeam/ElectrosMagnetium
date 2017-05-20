#!/usr/bin/env python

import logging
from serial import Serial, SerialException
from time import sleep


class ArduinoSerial(object):
    
    DEFAULT_BAUD = 115200
    _logger = logging.getLogger("ArduinoSerial")

    def __init__(self, scale=1):
        self._serial = Serial()
        self._scale = scale

    def _send_gcode(self, gcode):
        if gcode:
            self._logger.debug("sending gcode %s", gcode)
        gcode += "\n"
        self._serial.write("%s\n" % (gcode,))
        # Wait for grbl response with carriage return
        grbl_out = self._serial.readline().strip()
        if grbl_out:
            self._logger.debug("recived %s", grbl_out)

    def _go_to(self, point):
        """
        Send a command to the arduino to move the magnet to a specific (x, y)
        """
        self._logger.debug("going to %s", point)
        self._send_gcode("G90X%sY%s" % tuple(((self._scale * x) for x in point)))

    def _set_magnet_state(self, is_on):
        """
        Send a command to the arduino to activate/deactivate the magnet
        """
        self._logger.debug("turning magnet %s", "on" if is_on else "off")
        self._send_gcode("M3" if is_on else "M4")

    def open(self, port, baud=DEFAULT_BAUD):
        self._serial = Serial(port=port, baudrate=baud)
        # windows bug...
        try:
            self._serial.open()
        except SerialException:
            pass
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
    arduino_serial = ArduinoSerial()
    InteractiveShellEmbed(banner1="", confirm_exit=False, exit_msg="Bye :)")()
    arduino_serial.close()
