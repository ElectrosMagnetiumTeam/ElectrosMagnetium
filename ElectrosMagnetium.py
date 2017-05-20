#!/usr/bin/env python

from VoiceRecognition import VoiceRecognition
from VoiceOutput import VoiceOutput
from Games.Chess.ChessGame import ChessGame
from ArduinoSerial import ArduinoSerial
import logging
import argparse

# Physical board scale in CM
BOARD_SCALE = 30

def recognize_coords(vr, vo):
    while True:
        coord = vr.recognize().replace(" ", "").strip().upper()
        if len(coord) == 2 and ('A' <= coord[0] <= 'H') and ('1' <= coord[1] <= '8'):
            vo.say('Your coordinate was - {}'.format(coord))
            return coord

        vo.say('I did not understand the coordinate, please say it again')

def translate_coord(coord):
    return (ord(coord[0]) - ord('A'), ord(coord[1]) - ord('1'))

def play_game(vo, vr, hardware_interface):
    game = ChessGame(hardware_interface)
    print game
    
    while game.PLAYING == game.get_state():
        vo.say('It is team {}s turn'.format(game.get_turn_string()))

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
            print game

    if Game.TIE == game.get_state():
        vo.say('You have reached a tie by {}'.format(game.get_victory_string()[1]))
    else:
        vo.say('Player {} wins by {}'.format(*game.get_victory_string()))

def main(args):
    logging.basicConfig(level=logging.DEBUG)
    
    vo = VoiceOutput()
    vr = VoiceRecognition()

    hardware_interface = ArduinoSerial(port=args.port, scale=BOARD_SCALE)
    
    while True:
        vo.say('New game has begun')
        play_game(vo, vr, hardware_interface)

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--textual', dest='is_textual', action='store_true')
    parser.add_argument('--port', dest='port', type=str, default="")
    args = parser.parse_args() 
    print '[ArgumentParser] {}'.format(args)
    return args

if __name__ == '__main__':
    main(parse_args())
