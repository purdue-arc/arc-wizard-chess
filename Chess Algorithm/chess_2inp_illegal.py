#Wizard Chess
#version 1

'''
This program is supposed to compute a person's chess move
audibly spoken and play a chess game with it. It will then be 
used to control the robots to move in order to match the chess
move. In essence, this program's first task is to be able to play
a chess game, checking also for legal moves, based on two players
inputting their moves via text, using standard chess PGN text format.
'''

def printBoard(board):
    blackID = [' b ',' r ',' n ',' q ',' k ',' p ']
    print('\033[1;37;40m -------------------------------------------------')
    for i in range(0,8):
        for d in range(0,8):
            print(f"\033[1;37;40m |", end = "")
            if board[i][d] in blackID:
                print(f"\033[1;33;40m {board[i][d]}", end = "")
            else:
                print(f"\033[1;37;40m {board[i][d]}", end = "")
            #print('|', end = "")
            #print(board[i][d], end = "")
        print(f"\033[1;37;40m |")
        print(f"\033[1;37;40m -------------------------------------------------")
        #print('|')
        #print('---------------------------------')
    print("")

def computeMove(origPiece, move, turn, whitePieces, blackPieces, board):
    capture = False
    piece = move[0]
    if move[1] == 'x':
        capture = True
        col = move[2]
        row = move[3]
    else:
        col = move[1]
        row = move[2]
    colIndex = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f':5, 'g':6, 'h' : 7} 
    colLoc = colIndex[col]
    rowIndex = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3':5, '2':6, '1' : 7}
    rowLoc = rowIndex[row]
    if turn:
        pieceMove = whitePieces[piece]
    else:
        pieceMove = blackPieces[piece]
    board[rowLoc][colLoc] = pieceMove

    col = origPiece[1]
    row = origPiece[2]
    colLoc = colIndex[col]
    rowLoc = rowIndex[row]
    board[rowLoc][colLoc] = '   '
    
    return True
          
whiteR = ' R '
whiteN = ' N '
whiteB = ' B '
whiteQ = ' Q '
whiteK = ' K '
whiteP = ' P '

blackR = ' r '
blackN = ' n '
blackB = ' b '
blackQ = ' q '
blackK = ' k '
blackP = ' p '

whitePieces = {'R' : whiteR, 'N' : whiteN, 'B' : whiteB, 'Q' : whiteQ, 'K' : whiteK, 'P' : whiteP} 
blackPieces = {'R' : blackR, 'N' : blackN, 'B' : blackB, 'Q' : blackQ, 'K' : blackK, 'P' : blackP}

playerTurn = True # true if white's turn, false if black's turn
legal = True # make false if inputted move is illegal 
game = True # make false when game over
moveNum = 0

row8 = [' r ', ' n ', ' b ', ' q ', ' k ', ' b ', ' n ', ' r ']
row7 = [' p ', ' p ', ' p ', ' p ', ' p ', ' p ', ' p ', ' p ']
row6 = ['   ','   ','   ','   ','   ','   ','   ','   ']
row5 = ['   ','   ','   ','   ','   ','   ','   ','   ']
row4 = ['   ','   ','   ','   ','   ','   ','   ','   ']
row3 = ['   ','   ','   ','   ','   ','   ','   ','   ']
row2 = [' P ', ' P ', ' P ', ' P ', ' P ', ' P ', ' P ', ' P ']
row1 = [' R ', ' N ', ' B ', ' Q ', ' K ', ' B ', ' N ', ' R ']
board = [row8, row7, row6, row5, row4, row3, row2, row1]

print("\033[1;37;40m Start!")
print("")
printBoard(board)

while game and moveNum < 6:
    moveNum += 1
    print(f'\033[1;37;40m Move number: {moveNum}')
    inputPiece = input("\033[1;37;40m Piece location to move: ")
    inputMove = input("\033[1;37;40m Make a move: ")
    print("")
    print(f'\033[1;37;40m This is your move: {inputMove}')
    print("")
    legal = computeMove(inputPiece, inputMove, playerTurn, whitePieces, blackPieces, board)
    if legal:
        printBoard(board)
        if playerTurn:
            playerTurn = False
        else:
            playerTurn = True
    else:
        print("\033[1;37;40m Illegal move input")
        moveNum += -1