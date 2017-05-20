#!/usr/bin/env python

from VoiceRecognition import VoiceRecognition
from VoiceOutput import VoiceOutput
from Games.Chess.ChessGame import ChessGame
import time

# The board's scale in CM
BOARD_SCALE = 30

def recognize_coords(vr, vo):
    while True:
        coord = vr.recognize()
        if len(coord) == 2 and ('A' <= coord[0] <= 'H') and ('1' <= coord[1] <= '8'):
            return coord

        vo.say('I did not understand the coordinate, please say it again')

def main():
    vo = VoiceOutput()
    vr = VoiceRecognition()

    hardware_interface = ArduinoSerial(BOARD_SCALE)
    game = ChessGame(hardware_interface)

    while True:
        vo.say('Please state the source piece coordinate')
        source_coordinate = recognize_coords(vr, vo)

        vo.say('Please state the destination piece coordinate')
        dest_coordinate = recognize_coords(vr, vo)

        vo.say('You requested a move from {} to {}'.format(source_coordinate, dest_coordinate))

        game.move(*source_coordinate + dest_coordinate)

        time.sleep(4)

if __name__ == '__main__':
    main()
