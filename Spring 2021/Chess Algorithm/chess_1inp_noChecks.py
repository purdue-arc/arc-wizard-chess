#Wizard Chess
#version 2

'''
This program is supposed to compute a person's chess move
audibly spoken and play a chess game with it. It will then be 
used to control the robots to move in order to match the chess
move. In essence, this program's first task is to be able to play
a chess game, checking also for legal moves, based on two players
inputting their moves via text, using standard chess PGN text format.
'''

'''
Shit that needs to be coded so Nolan doesn't yell at me

castling
two of same piece that can go to input square (like two rooks on same row)
knight movement
en passant
checks
castling through check
checkmate
legal moves because of pins 
king capturing protected pieces
legal moves regarding dealing with checks and not moving into check
pawn promotion


easy stuff:
    castling -- short******** --- long******
    knight movement***************
    need to rewrite rook****** and queen******** code to check to see if the other piece can compute move if first one cant
    pawn promotion********
    en passant***********
    two same piece go to input square --- choose which piece to move***********
        //can happen for any piece because of promotion

hard stuff:
    checks
        //to get out of check, look at if inputted move blocks check
    checkmate
        //both checkmate and stalemate algorithms involve looking at 
            potential moves for next player to take
        
    legal moves regarding being in check, pins on king, 
        king capturing protected pieces, castling through checks
    stalemate
        //add flag for when just king maybe
        //have person say stalemate, then run checkForStalemate function
    draws because of insufficient material 
            //tally captures
            //at 28 ish captures, check to see what pieces are left 
            
also look into verifying computer correctly understood voice input of move before commanding robots
also might want to tell robot code as output of this chess code piece original location and piece new location per move
'''
'''
assumptions: 
    chess move input formmated correctly (especially if two same type pieces could move to square)
    pawns dont need two inputs
    two loc input only used when the specification is needed (aka if only one piece can make move, dont have two loc)
    two loc input always used if needed (e.g. never have one input if two same piece could move there)
    
    assume never three of same piece who can all move to same square where 2 on same col or row
'''

def printBoard(board):
    blackID = [' b ',' r ',' n ',' q ',' k ',' p ']
    print('\033[1;37;49m   COL-  A  -  B  -  C  -  D  -  E  -  F  -  G  -  H  -')
    print('\033[1;37;49mROW   ', end = "")
    print('\033[1;37;40m ------------------------------------------------')
    t = 8
    for i in range(0,8):
        print(f"\033[1;37;49m {t} : ", end = "")
        t += -1
        for d in range(0,8):
            
            print(f"\033[1;37;40m |", end = "")
            if board[i][d] in blackID:
                print(f"\033[1;34;40m {board[i][d]}", end = "")
            else:
                print(f"\033[1;33;40m {board[i][d]}", end = "")
            #print('|', end = "")
            #print(board[i][d], end = "")
        print(f"\033[1;37;40m |")
        print('\033[1;30;49m      ', end = "")
        print(f"\033[1;37;40m ------------------------------------------------")
        #print('|')
        #print('---------------------------------')
    print("")

def computeMove(move, turn, whitePieces, blackPieces, board):
    legal = False
    origC = ''
    origR = ''
    colIndex = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f':5, 'g':6, 'h' : 7} 
    rowIndex = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3':5, '2':6, '1' : 7}
    global enP
    if move == 'O-O':
        legal = shortCastle(board, turn)
        return legal
    elif move == 'O-O-O':
        legal = longCastle(board, turn)
        return legal
    piece = move[0]
    if piece != 'P':
        enP = False
    if move[1] in rowIndex:
        row = move[3]
        col = move[2]
        origR = move[1]
        legal = twoRow(board,colIndex[col], rowIndex[row], rowIndex[origR], turn, piece)
        return legal
    elif move[2] in colIndex:
        row = move[3]
        col = move[2]
        origC = move[1]
        if '=' in move:
            legal = twoCol(board, colIndex[col], rowIndex[row], colIndex[origC], turn, piece, move[5])
            return legal
        else:
            legal = twoCol(board, colIndex[col], rowIndex[row], colIndex[origC], turn, piece, False)
            return legal
    
    else:
        col = move[1]
        row = move[2]
    colLoc = colIndex[col]
    rowLoc = rowIndex[row]
    
    if turn:
        if board[rowLoc][colLoc] in piecesW:
            legal = False
            return legal
        else:
            pieceMove = whitePieces[piece]
    else:
        if board[rowLoc][colLoc] in piecesB:
            legal = False
            return legal
        else:
            pieceMove = blackPieces[piece]
            
    
    
    if move == 'O-O':
        legal = shortCastle(board, turn)
        return legal
    elif move == 'O-O-O':
        legal = longCastle(board, turn)
        return legal
    
    
    if '=' in move:
        if move[0] != 'P':
            legal = False
        else:
            #pawn promotion
            if '=' == move[3]:
                nP = move[4]
            elif '=' == move[4]:
                nP = move[5]
            if nP not in whitePieces or nP not in blackPieces:
                legal = False
                return legal
            
            if turn:
                newP = whitePieces[nP]
                if newP == ' K ' or newP == ' P ':
                    legal = False
                    return legal
            else:
                newP = blackPieces[nP]
                if newP == ' k ' or newP == ' p ':
                    legal = False
                    return legal
            enP = False
            legal = pawnPro(board, colLoc, rowLoc, turn, newP)
            return legal
 
        
    
    if piece == 'R':
        legal = moveRook(board, colLoc, rowLoc, turn)
    elif piece == 'P':
        legal = movePawn(board, colLoc, rowLoc, turn)
    elif piece == 'B':
        legal = moveBishop(board, colLoc, rowLoc, turn)
    elif piece == 'Q':
        legal = moveQueen(board, colLoc, rowLoc, turn)
    elif piece == 'K':
        legal = moveKing(board, colLoc, rowLoc, turn)
    elif piece == 'N':
        legal = moveKnight(board, colLoc, rowLoc, turn)
    else:
        legal = False
    
    # col = origPiece[1]
    # row = origPiece[2]
    # colLoc = colIndex[col]
    # rowLoc = rowIndex[row]
    # board[rowLoc][colLoc] = '   '
    
    
    if legal:
        board[rowLoc][colLoc] = pieceMove
        return legal
    
    
    

def moveRook(board, colIndex, rowIndex, turn):
    legal = False
    if turn:
        for r in range(0,8):
            if board[rowIndex][r] == ' R ':
                legal = True
                rookCol = r
                rookRow = rowIndex                
                if rookRow == rowIndex:
                    #rook moving horizontally
                    if rookCol < colIndex:
                        #rook moving right
                        for h in range(rookCol+1, colIndex):
                            if board[rowIndex][h] != '   ':
                                legal = False
                                break
                    else:
                        #rook moving left
                        for h in range(rookCol-1, colIndex, -1):
                            if board[rowIndex][h] != '   ':
                                legal = False
                                break
                else:
                    #rook moving vertically
                    if rookRow < rowIndex:
                        #rook moving up
                        for v in range(rookRow+1, rowIndex):
                            if board[v][colIndex] != '   ':
                                legal = False
                                break
                    else:
                        #rook moving down
                        for v in range(rookRow-1, rowIndex, -1):
                            if board[v][colIndex] != '   ':
                                legal = False
                                break
                if legal:
                    break
            else:
                legal = False
        if not legal:
            for c in range(0,8):
                if board[c][colIndex] == ' R ':
                    legal = True
                    rookCol = colIndex
                    rookRow = c
                    if rookRow == rowIndex:
                        #rook moving horizontally
                        if rookCol < colIndex:
                            #rook moving right
                            for h in range(rookCol+1, colIndex):
                                if board[rowIndex][h] != '   ':
                                    legal = False
                                    break
                        else:
                            #rook moving left
                            for h in range(rookCol-1, colIndex, -1):
                                if board[rowIndex][h] != '   ':
                                    legal = False
                                    break
                    else:
                        #rook moving vertically
                        if rookRow < rowIndex:
                            #rook moving up
                            for v in range(rookRow+1, rowIndex):
                                if board[v][colIndex] != '   ':
                                    legal = False
                                    break
                        else:
                            #rook moving down
                            for v in range(rookRow-1, rowIndex, -1):
                                if board[v][colIndex] != '   ':
                                    legal = False
                                    break
                    if legal:
                        break
                else:
                    legal = False
    else:
        for r in range(0,8):
            if board[rowIndex][r] == ' r ':
                legal = True
                rookCol = r
                rookRow = rowIndex                
                if rookRow == rowIndex:
                    #rook moving horizontally
                    if rookCol < colIndex:
                        #rook moving right
                        for h in range(rookCol+1, colIndex):
                            if board[rowIndex][h] != '   ':
                                legal = False
                                break
                    else:
                        #rook moving left
                        for h in range(rookCol-1, colIndex, -1):
                            if board[rowIndex][h] != '   ':
                                legal = False
                                break
                else:
                    #rook moving vertically
                    if rookRow < rowIndex:
                        #rook moving up
                        for v in range(rookRow+1, rowIndex):
                            if board[v][colIndex] != '   ':
                                legal = False
                                break
                    else:
                        #rook moving down
                        for v in range(rookRow-1, rowIndex, -1):
                            if board[v][colIndex] != '   ':
                                legal = False
                                break
                if legal:
                    break
            else:
                legal = False
        if not legal:
            for c in range(0,8):
                if board[c][colIndex] == ' r ':
                    legal = True
                    rookCol = colIndex
                    rookRow = c
                    if rookRow == rowIndex:
                        #rook moving horizontally
                        if rookCol < colIndex:
                            #rook moving right
                            for h in range(rookCol+1, colIndex):
                                if board[rowIndex][h] != '   ':
                                    legal = False
                                    break
                        else:
                            #rook moving left
                            for h in range(rookCol-1, colIndex, -1):
                                if board[rowIndex][h] != '   ':
                                    legal = False
                                    break
                    else:
                        #rook moving vertically
                        if rookRow < rowIndex:
                            #rook moving up
                            for v in range(rookRow+1, rowIndex):
                                if board[v][colIndex] != '   ':
                                    legal = False
                                    break
                        else:
                            #rook moving down
                            for v in range(rookRow-1, rowIndex, -1):
                                if board[v][colIndex] != '   ':
                                    legal = False
                                    break
                    if legal:
                        break
                else:
                    legal = False
    if not legal:
        return legal
    
    # if rookRow == rowIndex:
    #     #rook moving horizontally
    #     if rookCol < colIndex:
    #         #rook moving right
    #         for h in range(rookCol+1, colIndex):
    #             if board[rowIndex][h] != '   ':
    #                 legal = False
    #                 break
    #     else:
    #         #rook moving left
    #         for h in range(rookCol-1, colIndex, -1):
    #             if board[rowIndex][h] != '   ':
    #                 legal = False
    #                 break
    # else:
    #     #rook moving vertically
    #     if rookRow < rowIndex:
    #         #rook moving up
    #         for v in range(rookRow+1, rowIndex):
    #             if board[v][colIndex] != '   ':
    #                 legal = False
    #                 break
    #     else:
    #         #rook moving down
    #         for v in range(rookRow-1, rowIndex, -1):
    #             if board[v][colIndex] != '   ':
    #                 legal = False
    #                 break
    
    #still need to check about legal move regarding checks
    
    if rookCol == 7:
        if turn:
            global castleSW
            castleSW = False
        else:
            global castleSB
            castleSB = False
    elif rookCol == 0:
        if turn:
            global castleLW
            castleSW = False
        else:
            global castleLB
            castleSB = False
    
    if legal:
        board[rookRow][rookCol] = '   '
         
    return legal

def movePawn(board, colIndex, rowIndex, turn):
    '''
    Still need to do en passant --- check for first
    Also need to figure out when two pawns can take inputted square, make sure to choose right one
    '''
    legal = False
    if turn:
        if rowIndex == 0:
            return legal
    else:
        if rowIndex == 7:
            return legal
    global enP
    global enPR
    global enPC
    if enP:
        if rowIndex == enPR and colIndex == enPC:
            if turn:
                cP = ' P '
                if colIndex > 0 and board[rowIndex + 1][colIndex - 1] == cP:
                    board[rowIndex + 1][colIndex - 1] = '   '
                    board[rowIndex + 1][colIndex] = '   '
                    enP = False
                    legal = True
                    return legal
                elif colIndex < 7 and board[rowIndex + 1][colIndex + 1] == cP:
                    board[rowIndex + 1][colIndex + 1] = '   '
                    board[rowIndex + 1][colIndex] = '   '
                    enP = False
                    legal = True
                    return legal
                else:
                    legal = False
                    return legal
            else:
                cP = ' p '
                if colIndex > 0 and board[rowIndex - 1][colIndex - 1] == cP:
                    board[rowIndex - 1][colIndex - 1] = '   '
                    board[rowIndex - 1][colIndex] = '   '
                    enP = False
                    legal = True
                    return legal
                elif colIndex < 7 and board[rowIndex - 1][colIndex + 1] == cP:
                    board[rowIndex - 1][colIndex + 1] = '   '
                    board[rowIndex - 1][colIndex] = '   '
                    enP = False
                    legal = True
                    return legal
                else:
                    legal = False
                    return legal
            
        else:
            enP = False
    if not legal:
            
        if turn:
            sq1 = board[rowIndex + 1][colIndex]
            sq2 = board[rowIndex + 2][colIndex]
            if colIndex != 7:
                sq3 = board[rowIndex + 1][colIndex + 1]
            else:
                sq3 = '   '
            if colIndex != 0:
                sq4 = board[rowIndex + 1][colIndex - 1]
            else:
                sq4 = '   '
            
            if sq1 == '   ' and sq2 == '   ' and sq3 == '   ' and sq4 == '   ':
                legal = False
                return legal
    
            if board[rowIndex][colIndex] == '   ':
                if sq1 == '   ':
                    if sq2 != ' P ':
                        legal = False
                        return legal
                    else:
                        if rowIndex + 2 != 6:
                            legal = False
                            return legal
                        else:
                            board[rowIndex + 2][colIndex] = '   '
                            enP = True
                            enPR = rowIndex + 1
                            enPC = colIndex
                            legal = True
                elif sq1 != ' P ':
                    legal = False
                    return legal
                else:
                    board[rowIndex + 1][colIndex] = '   '
                    legal = True
            else:
                if sq3 != ' P ' and sq4 != ' P ':
                    legal = False
                    return legal
                elif sq3 == ' P ':
                    board[rowIndex + 1][colIndex + 1] = '   '
                    legal = True
                elif sq4 == ' P ':
                    board[rowIndex + 1][colIndex - 1] = '   '
                    legal = True
                
        else:
            sq1 = board[rowIndex - 1][colIndex]
            sq2 = board[rowIndex - 2][colIndex]
            if colIndex != 7:
                sq3 = board[rowIndex - 1][colIndex + 1]
            else:
                sq3 = '   '
            if colIndex != 0:
                sq4 = board[rowIndex - 1][colIndex - 1]
            else:
                sq4 = '   '
            
            if sq1 == '   ' and sq2 == '   ' and sq3 == '   ' and sq4 == '   ':
                legal = False
                return legal
            if board[rowIndex][colIndex] == '   ':
                if sq1 == '   ':
                    if sq2 != ' p ':
                        legal = False
                        return legal
                    else:
                        if rowIndex - 2 != 1:
                            legal = False
                            return legal
                        else:
                            board[rowIndex - 2][colIndex] = '   '
                            enP = True
                            enPR = rowIndex - 1
                            enPC = colIndex
                            legal = True
                elif sq1 != ' p ':
                    legal = False
                    return legal
                else:
                    board[rowIndex - 1][colIndex] = '   '
                    legal = True
            else:
                if sq3 != ' p ' and sq4 != ' p ':
                    legal = False
                    return legal
                elif sq3 == ' p ':
                    board[rowIndex - 1][colIndex + 1] = '   '
                    legal = True
                elif sq4 == ' p ':
                    board[rowIndex - 1][colIndex - 1] = '   '
                    legal = True
                    
        return legal

def moveBishop(board, colIndex, rowIndex, turn):
    legal = False
    r = rowIndex
    c = colIndex
    
    if turn:
        r = rowIndex + 1
        c = colIndex + 1
        while r < 8 and c < 8:
            if board[r][c] == ' B ':
                legal = True
                bishCol = c
                bishRow = r
                break
            elif board[r][c] != '   ':
                legal = False
                break                
            else:
                legal = False
                r += 1
                c += 1
        if not legal:
            r = rowIndex - 1
            c = colIndex + 1
            while r >= 0 and c < 8:
                if board[r][c] == ' B ':
                    legal = True
                    bishCol = c
                    bishRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += -1
                    c += 1
        if not legal:
            r = rowIndex - 1
            c = colIndex - 1
            while r >= 0 and c >= 0:
                if board[r][c] == ' B ':
                    legal = True
                    bishCol = c
                    bishRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += -1
                    c += -1
        if not legal:
            r = rowIndex + 1
            c = colIndex - 1
            while r < 8 and c >= 0:
                if board[r][c] == ' B ':
                    legal = True
                    bishCol = c
                    bishRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += 1
                    c += -1
    else:
        r = rowIndex + 1
        c = colIndex + 1
        while r < 8 and c < 8:
            if board[r][c] == ' b ':
                legal = True
                bishCol = c
                bishRow = r
                break
            elif board[r][c] != '   ':
                legal = False
                break                
            else:
                legal = False
                r += 1
                c += 1
        if not legal:
            r = rowIndex - 1
            c = colIndex + 1
            while r >= 0 and c < 8:
                if board[r][c] == ' b ':
                    legal = True
                    bishCol = c
                    bishRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += -1
                    c += 1
        if not legal:
            r = rowIndex - 1
            c = colIndex - 1
            while r >= 0 and c >= 0:
                if board[r][c] == ' b ':
                    legal = True
                    bishCol = c
                    bishRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += -1
                    c += -1
        if not legal:
            r = rowIndex + 1
            c = colIndex - 1
            while r < 8 and c >= 0:
                if board[r][c] == ' b ':
                    legal = True
                    bishCol = c
                    bishRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += 1
                    c += -1
    
    if not legal:
        return legal
    else:
        board[bishRow][bishCol] = '   '
        return legal

def moveQueen(board, colIndex, rowIndex, turn):
    legal = False
    r = rowIndex
    c = colIndex
    
    if turn:
        r = rowIndex + 1
        c = colIndex + 1
        while r < 8 and c < 8:
            if board[r][c] == ' Q ':
                legal = True
                queenCol = c
                queenRow = r
                break
            elif board[r][c] != '   ':
                legal = False
                break                
            else:
                legal = False
                r += 1
                c += 1
        if not legal:
            r = rowIndex - 1
            c = colIndex + 1
            while r >= 0 and c < 8:
                if board[r][c] == ' Q ':
                    legal = True
                    queenCol = c
                    queenRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += -1
                    c += 1
        if not legal:
            r = rowIndex - 1
            c = colIndex - 1
            while r >= 0 and c >= 0:
                if board[r][c] == ' Q ':
                    legal = True
                    queenCol = c
                    queenRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += -1
                    c += -1
        if not legal:
            r = rowIndex + 1
            c = colIndex - 1
            while r < 8 and c >= 0:
                if board[r][c] == ' Q ':
                    legal = True
                    queenCol = c
                    queenRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += 1
                    c += -1
    else:
        r = rowIndex + 1
        c = colIndex + 1
        while r < 8 and c < 8:
            if board[r][c] == ' q ':
                legal = True
                queenCol = c
                queenRow = r
                break
            elif board[r][c] != '   ':
                legal = False
                break                
            else:
                legal = False
                r += 1
                c += 1
        if not legal:
            r = rowIndex - 1
            c = colIndex + 1
            while r >= 0 and c < 8:
                if board[r][c] == ' q ':
                    legal = True
                    queenCol = c
                    queenRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += -1
                    c += 1
        if not legal:
            r = rowIndex - 1
            c = colIndex - 1
            while r >= 0 and c >= 0:
                if board[r][c] == ' q ':
                    legal = True
                    queenCol = c
                    queenRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += -1
                    c += -1
        if not legal:
            r = rowIndex + 1
            c = colIndex - 1
            while r < 8 and c >= 0:
                if board[r][c] == ' q ':
                    legal = True
                    queenCol = c
                    queenRow = r
                    break
                elif board[r][c] != '   ':
                    legal = False
                    break 
                else:
                    legal = False
                    r += 1
                    c += -1
    
    while not legal:
        if turn:
            cP = ' Q '
        else:
            cP = ' q '
        r = rowIndex + 1
        c = colIndex
        
        while r < 8:
            if board[r][c] == cP:
                queenRow = r
                queenCol = c
                legal = True
                break
            elif board[r][c] != '   ':
                legal = False
                break
            r += 1
            
        if legal:
            break
        
        r = rowIndex - 1
        c = colIndex 
        
        while r >= 0:
            if board[r][c] == cP:
                queenRow = r
                queenCol = c
                legal = True
                break
            elif board[r][c] != '   ':
                legal = False
                break
            r += -1
            
        if legal:
            break
        
        r = rowIndex
        c = colIndex + 1
        
        while c < 8:
            if board[r][c] == cP:
                queenRow = r
                queenCol = c
                legal = True
                break
            elif board[r][c] != '   ':
                legal = False
                break
            c += 1
        
        if legal:
            break
        
        r = rowIndex
        c = colIndex - 1
        
        while c >= 0:
            if board[r][c] == cP:
                queenRow = r
                queenCol = c
                legal = True
                break
            elif board[r][c] != '   ':
                legal = False
                break
            c += -1
        
        break
        
        
    
    # if not legal:
    #     if turn:
    #         for r in range(0,8):
    #             if board[rowIndex][r] == ' Q ':
    #                 legal = True
    #                 queenCol = r
    #                 queenRow = rowIndex                
    #                 break
    #             else:
    #                 legal = False
    #         if not legal:
    #             for c in range(0,8):
    #                 if board[c][colIndex] == ' Q ':
    #                     legal = True
    #                     queenCol = colIndex
    #                     queenRow = c
    #                     break
    #                 else:
    #                     legal = False
    #     else:
    #         for r in range(0,8):
    #             if board[rowIndex][r] == ' q ':
    #                 legal = True
    #                 queenCol = r
    #                 queenRow = rowIndex                
    #                 break
    #             else:
    #                 legal = False
    #         if not legal:
    #             for c in range(0,8):
    #                 if board[c][colIndex] == ' q ':
    #                     legal = True
    #                     queenCol = colIndex
    #                     queenRow = c
    #                     break
    #                 else:
    #                     legal = False
    #     if not legal:
    #         return legal
        
    #     if queenRow == rowIndex:
            
    #         if queenCol < colIndex:
                
    #             for h in range(queenCol+1, colIndex):
    #                 if board[rowIndex][h] != '   ':
    #                     legal = False
    #                     break
    #         else:
                
    #             for h in range(queenCol-1, colIndex, -1):
    #                 if board[rowIndex][h] != '   ':
    #                     legal = False
    #                     break
    #     else:
            
    #         if queenRow < rowIndex:
                
    #             for v in range(queenRow+1, rowIndex):
    #                 if board[v][colIndex] != '   ':
    #                     legal = False
    #                     break
    #         else:
                
    #             for v in range(queenRow-1, rowIndex, -1):
    #                 if board[v][colIndex] != '   ':
    #                     legal = False
    #                     break
    
    if not legal:
        return legal
    else:
        board[queenRow][queenCol] = '   '
        return legal
         
def moveKing(board, colIndex, rowIndex, turn):
    legal = False
    if turn:
        if rowIndex != 7 and colIndex != 7 and board[rowIndex + 1][colIndex + 1] == ' K ' :
            legal = True
            kingRow = rowIndex + 1
            kingCol = colIndex + 1
            
        elif rowIndex != 7 and board[rowIndex + 1][colIndex] == ' K ':
            legal = True
            kingRow = rowIndex + 1
            kingCol = colIndex
        elif rowIndex != 7 and colIndex != 0 and board[rowIndex + 1][colIndex -1] == ' K ':
            legal = True
            kingRow = rowIndex + 1
            kingCol = colIndex - 1
        elif rowIndex != 0 and colIndex != 7 and board[rowIndex - 1][colIndex + 1] == ' K ':
            legal = True
            kingRow = rowIndex - 1
            kingCol = colIndex + 1
        elif rowIndex != 0 and colIndex != 0 and board[rowIndex - 1][colIndex - 1] == ' K ':
            legal = True
            kingRow = rowIndex - 1
            kingCol = colIndex - 1    
        elif rowIndex != 0 and board[rowIndex - 1][colIndex] == ' K ':
            legal = True
            kingRow = rowIndex - 1
            kingCol = colIndex
        elif colIndex != 7 and board[rowIndex][colIndex + 1] == ' K ':
            legal = True
            kingRow = rowIndex
            kingCol = colIndex + 1
        elif colIndex != 0 and board[rowIndex][colIndex - 1] == ' K ':
            legal = True
            kingRow = rowIndex
            kingCol = colIndex - 1
        else:
            legal = False
            return legal
    else:
        if rowIndex != 7 and colIndex != 7 and board[rowIndex + 1][colIndex + 1] == ' k ' :
            legal = True
            kingRow = rowIndex + 1
            kingCol = colIndex + 1
            
        elif rowIndex != 7 and board[rowIndex + 1][colIndex] == ' k ':
            legal = True
            kingRow = rowIndex + 1
            kingCol = colIndex
        elif rowIndex != 7 and colIndex != 0 and board[rowIndex + 1][colIndex -1] == ' k ':
            legal = True
            kingRow = rowIndex + 1
            kingCol = colIndex - 1
        elif rowIndex != 0 and colIndex != 7 and board[rowIndex - 1][colIndex + 1] == ' k ':
            legal = True
            kingRow = rowIndex - 1
            kingCol = colIndex + 1
        elif rowIndex != 0 and colIndex != 0 and board[rowIndex - 1][colIndex - 1] == ' k ':
            legal = True
            kingRow = rowIndex - 1
            kingCol = colIndex - 1    
        elif rowIndex != 0 and board[rowIndex - 1][colIndex] == ' k ':
            legal = True
            kingRow = rowIndex - 1
            kingCol = colIndex
        elif colIndex != 7 and board[rowIndex][colIndex + 1] == ' k ':
            legal = True
            kingRow = rowIndex
            kingCol = colIndex + 1
        elif colIndex != 0 and board[rowIndex][colIndex - 1] == ' k ':
            legal = True
            kingRow = rowIndex
            kingCol = colIndex - 1
        else:
            legal = False
            return legal
    
    
    board[kingRow][kingCol] = '   '
    if turn:
        global castleSW 
        castleSW = False
        global castleLW
        castleLW = False
    else:
        global castleSB 
        castleSB = False
        global castleLB
        castleLB = False
    return legal

def moveKnight(board, colIndex, rowIndex, turn):
    legal = False
    
    if colIndex > 1 and rowIndex != 0:
        sp1 = board[rowIndex - 1][colIndex - 2]
    else:
        sp1 = '   '
    if colIndex > 0 and rowIndex > 1:
        sp2 = board[rowIndex - 2][colIndex - 1]
    else:
        sp2 = '   '
    if colIndex < 7 and rowIndex > 1:
        sp3 = board[rowIndex - 2][colIndex + 1]
    else:
        sp3 = '   '
    if colIndex < 6 and rowIndex != 0:
        sp4 = board[rowIndex - 1][colIndex + 2]
    else:
        sp4 = '   '
    if colIndex < 6 and rowIndex != 7:
        sp5 = board[rowIndex + 1][colIndex + 2]
    else:
        sp5 = '   '
    if colIndex < 7 and rowIndex < 6:
        sp6 = board[rowIndex + 2][colIndex + 1]
    else:
        sp6 = '   '
    if colIndex > 0 and rowIndex < 6:
        sp7 = board[rowIndex + 2][colIndex - 1]
    else:
        sp7 = '   '
    if colIndex > 1 and rowIndex != 7:
        sp8 = board[rowIndex + 1][colIndex - 2]
    else:
        sp8 = '   '
        
    sp = [sp1, sp2, sp3, sp4, sp5, sp6, sp7, sp8]
    
    if turn:
        cP = ' N '
    else:
        cP = ' n '
        
    for i in range(0,8):
        if cP == sp[i]:
            legal = True
            posNum = i + 1
            break
        else:
            legal = False
    
    if legal:
        if posNum == 1 or posNum == 4:
            r = rowIndex - 1
        elif posNum == 2 or posNum == 3:
            r = rowIndex - 2
        elif posNum == 5 or posNum == 8:
            r = rowIndex + 1
        elif posNum == 6 or posNum == 7:
            r = rowIndex + 2
        
        if posNum == 1 or posNum == 8:
            c = colIndex - 2
        elif posNum == 7 or posNum == 2:
            c = colIndex - 1
        elif posNum == 6 or posNum == 3:
            c = colIndex + 1
        elif posNum == 5 or posNum == 4:
            c = colIndex + 2
        
        board[r][c] = '   '
        
    return legal

def shortCastle(board, turn):
    if turn:
        global castleSW
        if not castleSW:
            return False
        else:
            if board[7][5] != '   ' or board[7][6] != '   ':
                return False
            else:
                board[7][5] = ' R '
                board[7][6] = ' K '
                board[7][4] = '   '
                board[7][7] = '   '
                return True
    else:
        global castleSB
        if not castleSB:
            return False
        else:
            if board[0][5] != '   ' or board[0][6] != '   ':
                return False
            else:
                board[0][5] = ' r '
                board[0][6] = ' k '
                board[0][4] = '   '
                board[0][7] = '   '
                return True
    
def longCastle(board, turn):
    if turn:
        global castleLW
        if not castleLW:
            return False
        else:
            if board[7][1] != '   ' or board[7][2] != '   ' or board[7][3] != '   ':
                return False
            else:
                board[7][3] = ' R '
                board[7][2] = ' K '
                board[7][4] = '   '
                board[7][0] = '   '
                return True
    else:
        global castleLB
        if not castleLB:
            return False
        else:
            if board[0][1] != '   ' or board[0][2] != '   ' or board[0][3] != '   ':
                return False
            else:
                board[0][3] = ' r '
                board[0][2] = ' k '
                board[0][4] = '   '
                board[0][0] = '   '
                return True

def pawnPro(board, c, r, turn, nP):
    #first, determine which pawn to look for
    legal = False
    if turn:
        cP = ' P '
    else:
        cP = ' p '
    #next, determine if pawn capture or not
    if board[r][c] == '   ':
        cap = False
    else:
        cap = True
    
    if turn and r == 0:
        if cap:
            #check diagonal squares
            oC = c - 1
            oR = r + 1
            if oC >= 0 and board[oR][oC] == cP:
                legal = True
                board[r][c] = nP
                board[oR][oC] = '   '
                return legal
            else:
                oC = c + 1
                if oC < 8 and board[oR][oC] == cP:
                    legal = True
                    board[r][c] = nP
                    board[oR][oC] = '   '
                    return legal
                else:
                    legal = False
                    return legal
        else:
            if board[r+1][c] == cP:
                legal = True
                board[r][c] = nP
                board[r+1][c] = '   '
                return legal
            else:
                legal = False
                return legal
    elif not turn and r == 7:
        if cap:
            #check diagonal squares
            oC = c - 1
            oR = r - 1
            if oC >= 0 and board[oR][oC] == cP:
                legal = True
                board[r][c] = nP
                board[oR][oC] = '   '
                return legal
            else:
                oC = c + 1
                if oC < 8 and board[oR][oC] == cP:
                    legal = True
                    board[r][c] = nP
                    board[oR][oC] = '   '
                    return legal
                else:
                    legal = False
                    return legal
        else:
            if board[r-1][c] == cP:
                legal = True
                board[r][c] = nP
                board[r-1][c] = '   '
                return legal
            else:
                legal = False
                return legal
    else:
        legal = False
        return legal

def twoCol(board, c, r, oC, turn, p, pro):
    legal = False
    if turn:
        if board[r][c] in piecesW:
            legal = False
            return legal
        else:
            pieceMove = whitePieces[p]
    else:
        if board[r][c] in piecesB:
            legal = False
            return legal
        else:
            pieceMove = blackPieces[p]
    if pro:
        #pawn promotion from specificed col
        if board[r][c] == '   ':
            #pawn diagonal movement illegal
            legal = False
            return legal
        if turn:
            cP = ' P '
            oR = r + 1
            if r != 0:
                legal = False
                return legal
        else:
            cP = ' p '
            oR = r - 1
            if r != 7:
                legal = False
                return legal
        if board[oR][oC] == cP:
            board[oR][oC] = '   '
            legal = True
            pieceMove = whitePieces[pro] if turn else blackPieces[pro]
        else:
            legal = False
            return legal
    else:
        #every other kind of move, p = piece inputted
        if p == 'P':
            global enP
            global enPR
            global enPC
            if enP:
                rowIndex = r
                colIndex = c
                if rowIndex == enPR and colIndex == enPC:
                    print(2)
                    if turn:
                        cP = ' P '
                        if board[rowIndex + 1][oC] == cP:
                            board[rowIndex + 1][oC] = '   '
                            board[rowIndex + 1][colIndex] = '   '
                            enP = False
                            legal = True
                            
                        else:
                            legal = False
                            return legal
                    else:
                        cP = ' p '
                        if board[rowIndex - 1][oC] == cP:
                            board[rowIndex - 1][oC] = '   '
                            board[rowIndex - 1][colIndex] = '   '
                            enP = False
                            legal = True
                            
                            
                        else:
                            legal = False
                            return legal
                    
                else:
                    enP = False
            if not legal:
                cP = ' P ' if turn else ' p '
                if board[r][c] == '   ':
                    legal = False
                    return legal
                else:
                    oR = r + 1 if turn else r - 1
                    if board[oR][oC] != cP:
                        legal = False
                        return legal
                    else:
                        board[oR][oC] = '   '
                        legal = True
        elif p == 'R':
            cP = ' R ' if turn else ' r '
            if board[r][oC] != cP:
                legal = False
                return legal
            else:
                if oC > c:
                    #rook moving left
                    tC = c + 1
                    while tC < oC:
                        if board[r][tC] != '   ':
                            legal = False
                            return legal
                        else:
                            tC += 1
                elif oC < c:
                    tC = c - 1
                    while tC > oC:
                        if board[r][tC] != '   ':
                            legal = False
                            return legal
                        else:
                            tC += -1
                else:
                    legal = False
                    return legal
                legal = True
                board[r][oC] = '   '
        elif p == 'N':
            cP = ' N ' if turn else ' n '
            if abs(c - oC) == 1:
                if r + 2 < 8 and board[r+2][oC] == cP:
                    found = True
                    oR = r + 2
                elif r - 2 >= 0 and board[r-2][oC] == cP:
                    found = True
                    oR = r - 2
            elif abs(c - oC) == 2:
                if r + 1 < 8 and board[r+1][oC] == cP:
                    found = True
                    oR = r + 1
                elif r - 1 >= 0 and board[r-1][oC] == cP:
                    found = True
                    oR = r - 1
            else:
                legal = False
                return legal
            
            if found:
                legal = True
                board[oR][oC] = '   '
            else:
                legal = False
                return legal
        elif p == 'B':
            cP = ' B ' if turn else ' b '
            dist = abs(c - oC)
            r1 = r + dist
            r2 = r - dist
            if r1 < 8 and board[r1][oC] == cP:
                oR = r1
                tC = oC - 1 if oC > c else oC + 1
                r1 += -1
                while r1 != r and tC != c:
                    if board[r1][tC] != '   ':
                        legal = False
                        return legal
                    r1 += -1
                    tC = tC - 1 if oC > c else tC + 1
            elif r2 >= 0 and board[r2][oC] == cP:
                oR = r2
                tC = oC - 1 if oC > c else oC + 1
                r2 += 1
                while r2 != r and tC != c:
                    if board[r2][tC] != '   ':
                        legal = False
                        return legal
                    r2 += 1
                    tC = tC - 1 if oC > c else tC + 1
            else:
                legal = False
                return legal
                    
            legal = True
            board[oR][oC] = '   '
            
        elif p == 'Q':
            #three squares to check given col: horizontal, diagonal up, diagonal down
            cP = ' Q ' if turn else ' q ' 
            if board[r][oC] == cP:
                if oC > c:
                    for tC in range(oC - 1, c, -1):
                        if board[r][tC] != '   ':
                            legal = False
                            return legal
                elif oC < c:
                    for tC in range(oC + 1, c):
                        if board[r][tC] != '   ':
                            legal = False
                            return legal
                else:
                    legal = False
                    return legal
                oR = r
            else:
                dist = abs(c - oC)
                r1 = r + dist
                r2 = r - dist
                if r1 < 8 and board[r1][oC] == cP:
                    oR = r1
                    tC = oC - 1 if oC > c else oC + 1
                    r1 += -1
                    while r1 != r and tC != c:
                        if board[r1][tC] != '   ':
                            legal = False
                            return legal
                        r1 += -1
                        tC = tC - 1 if oC > c else tC + 1
                elif r2 >= 0 and board[r2][oC] == cP:
                    oR = r2
                    tC = oC - 1 if oC > c else oC + 1
                    r2 += 1
                    while r2 != r and tC != c:
                        if board[r2][tC] != '   ':
                            legal = False
                            return legal
                        r2 += 1
                        tC = tC - 1 if oC > c else tC + 1
                else:
                    legal = False
                    return legal
            
            legal = True
            board[oR][oC] = '   '
            
        else:
            legal = False
            return legal
        
        if legal:
            board[r][c] = pieceMove
            return legal
        else:
            return legal
                
def twoRow(board, c, r, oR, turn, p):
    legal = False
    if turn:
        if board[r][c] in piecesW:
            legal = False
            return legal
        else:
            pieceMove = whitePieces[p]
    else:
        if board[r][c] in piecesB:
            legal = False
            return legal
        else:
            pieceMove = blackPieces[p]
    if p == 'P':
        legal = False
        return legal
    elif p == 'R':
        cP = ' R ' if turn else ' r '
        if board[oR][c] != cP:
            legal = False
            return legal
        else:
            if oR > r:
                #rook moving up
                tR = r + 1
                while tR < oR:
                    if board[tR][c] != '   ':
                        legal = False
                        return legal
                    else:
                        tR += 1
            elif oR < r:
                tR = r - 1
                while tR > oR:
                    if board[tR][c] != '   ':
                        legal = False
                        return legal
                    else:
                        tR += -1
            else:
                legal = False
                return legal
            legal = True
            board[oR][c] = '   '
    elif p == 'N':
        cP = ' N ' if turn else ' n '
        if abs(r - oR) == 1:
            if c + 2 < 8 and board[oR][c+2] == cP:
                found = True
                oC = c + 2
            elif c - 2 >= 0 and board[oR][c-2] == cP:
                found = True
                oC = c - 2
        elif abs(r - oR) == 2:
            if c + 1 < 8 and board[oR][c+1] == cP:
                found = True
                oC = c + 1
            elif c - 1 >= 0 and board[oR][c-1] == cP:
                found = True
                oC = c - 1
        else:
            legal = False
            return legal
        
        if found:
            legal = True
            board[oR][oC] = '   '
        else:
            legal = False
            return legal
    elif p == 'B':
        cP = ' B ' if turn else ' b '
        dist = abs(r - oR)
        c1 = c + dist
        c2 = c - dist
        if c1 < 8 and board[oR][c1] == cP:
            oC = c1
            tR = oR - 1 if oR > r else oR + 1
            c1 += -1
            while c1 != c and tR != r:
                if board[tR][c1] != '   ':
                    legal = False
                    return legal
                c1 += -1
                tR = tR - 1 if oR > r else tR + 1
        elif c2 >= 0 and board[oR][c2] == cP:
            oC = c2
            tR = oR - 1 if oR > r else oR + 1
            c2 += 1
            while c2 != c and tR != r:
                if board[tR][c2] != '   ':
                    legal = False
                    return legal
                c2 += 1
                tR = tR - 1 if oR > r else tR + 1
        else:
            legal = False
            return legal
                
        legal = True
        board[oR][oC] = '   '
        
    elif p == 'Q':
        #three squares to check given col: vertical, diagonal up, diagonal down
        cP = ' Q ' if turn else ' q ' 
        if board[oR][c] == cP:
            if oR > r:
                for tR in range(oR - 1, r, -1):
                    if board[tR][c] != '   ':
                        legal = False
                        return legal
            elif oR < r:
                for tR in range(oR + 1, r):
                    if board[tR][c] != '   ':
                        legal = False
                        return legal
            else:
                legal = False
                return legal
            oC = c
        else:
            dist = abs(r - oR)
            c1 = c + dist
            c2 = c - dist
            if c1 < 8 and board[oR][c1] == cP:
                oC = c1
                tR = oR - 1 if oR > r else oR + 1
                c1 += -1
                while c1 != c and tR != r:
                    if board[tR][c1] != '   ':
                        legal = False
                        return legal
                    c1 += -1
                    tR = tR - 1 if oR > r else tR + 1
            elif c2 >= 0 and board[oR][c2] == cP:
                oC = c2
                tR = oR - 1 if oR > r else oR + 1
                c2 += 1
                while c2 != c and tR != r:
                    if board[tR][c2] != '   ':
                        legal = False
                        return legal
                    c2 += 1
                    tR = tR - 1 if oR > r else tR + 1
            else:
                legal = False
                return legal
        
        legal = True
        board[oR][oC] = '   '
        
    else:
        legal = False
        return legal
    
    if legal:
        board[r][c] = pieceMove
        return legal
    else:
        return legal








whiteR = ' R '
whiteN = ' N '
whiteB = ' B '
whiteQ = ' Q '
whiteK = ' K '
whiteP = ' P '

piecesW = [whiteR, whiteN, whiteB, whiteQ, whiteK, whiteP]

blackR = ' r '
blackN = ' n '
blackB = ' b '
blackQ = ' q '
blackK = ' k '
blackP = ' p '

piecesB = [blackR, blackN, blackB, blackQ, blackK, blackP]

whitePieces = {'R' : whiteR, 'N' : whiteN, 'B' : whiteB, 'Q' : whiteQ, 'K' : whiteK, 'P' : whiteP} 
blackPieces = {'R' : blackR, 'N' : blackN, 'B' : blackB, 'Q' : blackQ, 'K' : blackK, 'P' : blackP}

castleSB = True
castleSW = True
castleLB = True
castleLW = True
enP = False
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

print("")
print("Start!")
print("")
printBoard(board)

while game and moveNum < 1:
    moveNum += 1
    print(f'Move number: {moveNum}')
    #inputPiece = input("\033[1;37;40m Piece location to move: ")
    inputMove = input("Make a move: ")
    print("")
    print(f'This is your move: {inputMove}')
    print("")
    legal = computeMove(inputMove, playerTurn, whitePieces, blackPieces, board)
    if legal:
        printBoard(board)
        if playerTurn:
            playerTurn = False
        else:
            playerTurn = True
    else:
        print("Illegal move input")
        contQ = input("Try again? ")
        if ('Yes' in contQ) or ('yes' in contQ):
            moveNum += -1
        else:
            game = False
    