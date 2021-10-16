# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 18:46:06 2021

@author: broat
"""

import chess as ch
import VoiceTest

#initialize FEN board
#board = ch.Board("K7/8/8/8/8/8/5Q2/7k b KQkq - 0 2") #stalemate test
#board = ch.Board("rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2") #checkmate test
board = ch.Board() #default board
print(board)
turnNum = 0

#game loop
while (board.is_check() != True and board.is_stalemate() != True):
    if(turnNum % 2 == 0):
        print("\nWhite's move")
    else:
        print("\nBlack's move")
        
    startSpace, endSpace = VoiceTest.getMoveAudio()
    move_to_make = str(startSpace[0] + startSpace[1] + endSpace[0] + endSpace[1])
    
    try:
        board.push_san(move_to_make)
        turnNum += 1
    except ValueError:
        print("Invalid move, please try again\n")
        VoiceTest.getMoveAudio
        
    print(board)

#win statement
if(board.is_stalemate() == True):
    print("\nIt's a draw!")
elif(turnNum % 2 == 0):
    print("\nWhite wins!")
else:
    print("\nBlack wins!")
