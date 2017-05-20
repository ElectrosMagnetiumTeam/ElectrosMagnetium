#!/usr/bin/env python

from VoiceRecognition import VoiceRecognition
from VoiceOutput import VoiceOutput
from Games.Chess.ChessGame import ChessGame
from ArduinoSerial import ArduinoSerial
import logging

# Physical board scale in CM
BOARD_SCALE = 30

def recognize_coords(vr, vo):
    while True:
        coord = vr.recognize()
        if len(coord) == 2 and ('A' <= coord[0] <= 'H') and ('1' <= coord[1] <= '8'):
            return coord

        vo.say('I did not understand the coordinate, please say it again')

def translate_coord(coord):
    return (ord(coord[0]) - ord('A'), ord(coord[1]) - ord('1'))

def main():
    vo = VoiceOutput()
    vr = VoiceRecognition()

    hardware_interface = ArduinoSerial(BOARD_SCALE)
    game = ChessGame(hardware_interface)

    
    logging.basicConfig(level=logging.DEBUG)
    
    while True:
        vo.say('Please state the source piece coordinate')
        source_coordinate = recognize_coords(vr, vo)

        vo.say('Please state the destination piece coordinate')
        dest_coordinate = recognize_coords(vr, vo)

        vo.say('You requested a move from {} to {}'.format(source_coordinate, dest_coordinate))

        move_ok = game.move(*(translate_coord(source_coordinate) + 
                              translate_coord(dest_coordinate)))
        
        if not move_ok:
            vo.say('Your move was illegal')
        else:
            vo.say('Your move was done')

if __name__ == '__main__':
    main()
