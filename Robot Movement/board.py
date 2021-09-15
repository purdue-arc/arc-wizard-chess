'''
figure out implement turning based on input angle
    need a function that accepts angle as input --- radians (pos == clockwise)
    turnRobot(angle)
        return True
    
figure out moving forward while oriented at input angle
    need function that accepts two velocities
    moveForward(distance) -- center to center
        return True
    
flowchart
    robot control: figure out angle and distance to move
    board: turn robot inputted angle
           move robot forward distance meters
           turn robot neg inputted angle
    
'''

import pygame
import time
import numpy as np

global size
global gameDisplay

'''
NOTES

haven't tested movement of black pieces
need to alter code for getTriPoints for black pieces
need to implement wait for next move
'''

def printBoard():
            #set color with rgb
            white,black = (255,255,255),(0,0,0)
            
            #set display
            global gameDisplay
            gameDisplay = pygame.display.set_mode((600,600))
            #Size of squares
            global size 
            size = 50
            
            #board length, must be even
            boardLength = 8
            gameDisplay.fill(white)
            
            cnt = 0
            for i in range(1,boardLength+1):
                for z in range(1,boardLength+1):
                    #check if current loop value is even
                    if cnt % 2 == 0:
                        pygame.draw.rect(gameDisplay, white,[size*z,size*i,size,size])
                    else:
                        pygame.draw.rect(gameDisplay, black, [size*z,size*i,size,size])
                    cnt +=1
                #since theres an even number of squares go back one value
                cnt-=1
            #Add a nice boarder
            pygame.draw.rect(gameDisplay,black,[size,size,boardLength*size,boardLength*size],1)
            pygame.display.update()

def printPiece(head, lB, rB):
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    if head[1] < lB[1]:
        color = red
    else:
        color = blue
    
    pygame.draw.polygon(gameDisplay, color, (head,lB,rB))
    pygame.draw.circle(gameDisplay, green, head, 5, 0)
    pygame.display.update()

def timeStep(seconds=0.25):
    start_time = time.time()
    

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
    
        if elapsed_time > seconds:
            break

def turnRobot(ang, p1, direction,pieceLoc):
    #ang == angle to turn in radians; pos -> counterclockwise
    #head == current pos of head vertex
    #lB == current pos of left base vertex
    #rB == current pos of right base vertex
    head = p1[0]
    lB = p1[1]
    rB = p1[2]
    time = 20
    if direction > 0:
        if ang > 0:
            #turning clockwise; lB doesnt change
            step = ang / time
            base = np.sqrt((abs(lB[0] - rB[0]))**2 + (abs(lB[1] - rB[1]))**2)
            side = np.sqrt((abs(lB[0] - head[0]))**2 + (abs(lB[1] - head[1]))**2)
            angH = np.arccos(base/2/side)
            height = side * np.sin(angH)
            angle = step
            for i in range(0,time+1):
                #only works right now for angles less than 90 degrees
                rx = lB[0] + (base * np.cos(angle))
                ry = lB[1] - (base * np.sin(angle))
                rB = (rx,ry)
                p1[2] = rB
                hx = lB[0] + (side * np.cos(angle+angH))
                hy = lB[1] - (side * np.sin(angle+angH))
                head = (hx,hy)
                # cB = (lB[0] + abs(rB[0] - lB[0])/2, lB[1] - abs(rB[1] - lB[1])/2)
                # hx = cB[0] - height * np.sin(angle)
                # hy = cB[1] - height * np.cos(angle)
                head = (hx,hy)
                p1[0] = head
                angle += step
                printBoard()
                printPieces(pieceLoc)
                timeStep()
        elif ang < 0:
            #turning clockwise; lB doesnt change
            ang = abs(ang)
            step = ang / time
            base = np.sqrt((abs(lB[0] - rB[0]))**2 + (abs(lB[1] - rB[1]))**2)
            side = np.sqrt((abs(lB[0] - head[0]))**2 + (abs(lB[1] - head[1]))**2)
            angH = np.arccos(base/2/side)
            height = side * np.sin(angH)
            angle = step
            for i in range(0,time+1):
                #only works right now for angles less than 90 degrees
                lx = rB[0] - (base * np.cos(angle))
                ly = rB[1] - (base * np.sin(angle))
                lB = (lx,ly)
                p1[1] = lB
                hx = rB[0] - (side * np.cos(angle+angH))
                hy = rB[1] - (side * np.sin(angle+angH))
                head = (hx,hy)
                p1[0] = head
                # cB = (lB[0] + abs(rB[0] - lB[0])/2, lB[1] - abs(rB[1] - lB[1])/2)
                # hx = cB[0] - height * np.sin(angle)
                # hy = cB[1] - height * np.cos(angle)
                head = (hx,hy)
                angle += step
                printBoard()
                printPieces(pieceLoc)
                timeStep()
    elif direction < 0:
        if ang > 0:
            #turning clockwise; lB doesnt change
            ang = abs(ang)
            step = ang / time
            base = np.sqrt((abs(lB[0] - rB[0]))**2 + (abs(lB[1] - rB[1]))**2)
            side = np.sqrt((abs(lB[0] - head[0]))**2 + (abs(lB[1] - head[1]))**2)
            angH = np.arccos(base/2/side)
            height = side * np.sin(angH)
            angle = ang
            # angle = step
            for i in range(0,time+1):
                #only works right now for angles less than 90 degrees
                lx = rB[0] - (base * np.cos(angle))
                ly = rB[1] - (base * np.sin(angle))
                lB = (lx,ly)
                p1[1] = lB
                hx = rB[0] - (side * np.cos(angle+angH))
                hy = rB[1] - (side * np.sin(angle+angH))
                
                head = (hx,hy)
                p1[0] = head
                # cB = (lB[0] + abs(rB[0] - lB[0])/2, lB[1] - abs(rB[1] - lB[1])/2)
                # hx = cB[0] - height * np.sin(angle)
                # hy = cB[1] - height * np.cos(angle)
                head = (hx,hy)
                angle += -1*step
                printBoard()
                printPieces(pieceLoc)
                timeStep()
        elif ang < 0:
            #turning clockwise; lB doesnt change
            ang = abs(ang)
            step = ang / time
            base = np.sqrt((abs(lB[0] - rB[0]))**2 + (abs(lB[1] - rB[1]))**2)
            side = np.sqrt((abs(lB[0] - head[0]))**2 + (abs(lB[1] - head[1]))**2)
            angH = np.arccos(base/2/side)
            height = side * np.sin(angH)
            angle = ang
            for i in range(0,time+1):
                #only works right now for angles less than 90 degrees
                rx = lB[0] + (base * np.cos(angle))
                ry = lB[1] - (base * np.sin(angle))
                rB = (rx,ry)
                p1[2] = rB
                hx = lB[0] + (side * np.cos(angle+angH))
                hy = lB[1] - (side * np.sin(angle+angH))
                head = (hx,hy)
                p1[0] = head
                # cB = (lB[0] + abs(rB[0] - lB[0])/2, lB[1] - abs(rB[1] - lB[1])/2)
                # hx = cB[0] - height * np.sin(angle)
                # hy = cB[1] - height * np.cos(angle)
                head = (hx,hy)
                angle += -1*step
                printBoard()
                printPieces(pieceLoc)
                timeStep()
    return (head,lB,rB)

def moveForward(dist, p1, direction, ang,pieceLoc):
    head = p1[0]
    lB = p1[1]
    rB = p1[2]
    time = 20
    if direction > 0:
        #moving forward
        step = dist / time
        for i in range(0,time):
            lx = lB[0] - np.sin(ang) * step
            ly = lB[1] - np.cos(ang) * step
            rx = rB[0] - np.sin(ang) * step
            ry = rB[1] - np.cos(ang) * step
            hx = head[0] - np.sin(ang) * step
            hy = head[1] - np.cos(ang) * step
            lB = (lx,ly)
            rB = (rx,ry)
            head = (hx,hy)
            p1[0] = head
            p1[1] = lB
            p1[2] = rB
            printBoard()
            printPieces(pieceLoc)
            timeStep()
            
            
    elif direction < 0:
        #moving backwards
        step = dist / time
        for i in range(0,time):
            lx = lB[0] + np.sin(ang) * step
            ly = lB[1] + np.cos(ang) * step
            rx = rB[0] + np.sin(ang) * step
            ry = rB[1] + np.cos(ang) * step
            hx = head[0] + np.sin(ang) * step
            hy = head[1] + np.cos(ang) * step
            lB = (lx,ly)
            rB = (rx,ry)
            head = (hx,hy)
            p1[0] = head
            p1[1] = lB
            p1[2] = rB
            printBoard()
            printPieces(pieceLoc)
            timeStep()
            
    return (head, lB, rB)

def moveRobot(pieceLoc, p1, ang, dist, direction):
    #direction == 1 if moving forward, -1 if moving backward
    for i in pieceLoc:
        if i == p1:
            found = True
            break
        else:
            found = False
    if not found:
        print("Piece not found on board")
        return
    
    printBoard()
    printPieces(pieceLoc)
    pos = moveForward(10,p1,1,0,pieceLoc)
    p1[0] = pos[0]
    p1[1] = pos[1]
    p1[2] = pos[2]
    pos = turnRobot(ang,p1,1,pieceLoc)
    p1[0] = pos[0]
    p1[1] = pos[1]
    p1[2] = pos[2]
    timeStep()
    pos = moveForward(dist, p1, direction, ang,pieceLoc)
    timeStep()
    p1[0] = pos[0]
    p1[1] = pos[1]
    p1[2] = pos[2]
    ang = -1 * ang
    pos = turnRobot(ang,p1, -1,pieceLoc)
    p1[0] = pos[0]
    p1[1] = pos[1]
    p1[2] = pos[2]
    pos = moveForward(10,p1,-1,0,pieceLoc)
    p1[0] = pos[0]
    p1[1] = pos[1]
    p1[2] = pos[2]

def printPieces(pieceLoc): #pieceLoc is list containing a list for each piece's location points
    for piece in pieceLoc:
        printPiece(piece[0],piece[1],piece[2])
    pygame.display.update()

def getTriPoints(coord, color): #coord in form [row,col]
    c = coord[0]
    r = coord[1]
    
    if color == 'white':
        head = ((r+1+0.5)*size, (c+1+0.2)*size)
        lB = ((r+1+0.2)*size,(c+1+0.8)*size)
        rB = ((r+1+0.8)*size,(c+1+0.8)*size)
    elif color == 'black':
        head = ((r+1+0.5)*size, (c+1+0.8)*size)
        rB = ((r+1+0.2)*size,(c+1+0.2)*size)
        lB = ((r+1+0.8)*size,(c+1+0.2)*size)
    p1 = [head,lB,rB]
    return p1

def setPieces(pieceLoc):
    for i in range(0,8):
        for j in range(6,8):
            p = getTriPoints([j,i], 'white')
            pieceLoc.append(p)
    for i in range(0,8):
        for j in range(0,2):
            p = getTriPoints([j,i],'black')
            pieceLoc.append(p)
    return pieceLoc

def moveWheels(lV, rV, pieceLoc, p1, color):
    #lV = velocity for left wheel
    #rV = velocity for right wheel
    #think about making velocities list where each value represents 1 second
    
    base = np.sqrt((abs(p1[1][0] - p1[2][0]))**2 + (abs(p1[1][1] - p1[2][1]))**2)
    if color == 'white':
        for l, r in zip(lV,rV):
            printBoard()
            printPieces(pieceLoc)
            timeStep(1)
            if abs(l) > abs(r): #moving to the right
                r1 = (base * r) / (l - r)
                r2 = base + r1
                r3 = np.sqrt((base)**2 + (base/2 + r1)**2)
                ang = l / r2
                
                angAxis = np.arctan((p1[2][1] - p1[1][1]) / (p1[2][0] - p1[1][0]))
                cX = r1 * np.cos(angAxis) + p1[2][0]
                cY = r1 * np.sin(angAxis) + p1[2][1]
                angh = abs(np.arctan((p1[0][1] - cY) / (p1[0][0] - cX)))
                rX = cX - r1 * np.cos(ang + angAxis)
                rY = cY - r1 * np.sin(ang + angAxis)
                lX = cX - r2 * np.cos(ang + angAxis)
                lY = cY - r2 * np.sin(ang+angAxis)
                hX = cX - r3 * np.cos(ang + angh) 
                hY = cY - r3 * np.sin(ang + angh)
                p1[0] = (hX,hY)
                p1[1] = (lX,lY)
                p1[2] = (rX,rY)
            elif abs(l) < abs(r): #moving to the left
                r1 = (base * l) / (r-l)
                r2 = base + r1
                r3 = np.sqrt((base)**2 + (base/2 + r1)**2)
                ang = r / r2
                
                angAxis = np.arctan((p1[1][1] - p1[2][1]) / (p1[2][0] - p1[1][0]))
                cX = -r1 * np.cos(angAxis) + p1[1][0]
                cY = r1 * np.sin(angAxis) + p1[1][1]
                angh = abs(np.arctan((p1[0][1] - cY) / (p1[0][0] - cX)))
                rX = cX + r2 * np.cos(ang + angAxis)
                rY = cY - r2 * np.sin(ang + angAxis)
                lX = cX + r1 * np.cos(ang + angAxis)
                lY = cY - r1 * np.sin(ang + angAxis)
                hX = cX + r3 * np.cos(ang + angh) 
                hY = cY - r3 * np.sin(ang + angh)
                
                p1[0] = (hX,hY)
                p1[1] = (lX,lY)
                p1[2] = (rX,rY)
            else: #moving forward/backward
                ang = np.arccos((p1[2][0]-p1[1][0]) / base)
                ang = ang if p1[2][1] < p1[1][1] else -1*ang #pos angle -> turning left
                lx = p1[1][0] - np.sin(ang) * l
                ly = p1[1][1] - np.cos(ang) * l
                rx = p1[2][0] - np.sin(ang) * r
                ry = p1[2][1] - np.cos(ang) * r
                hx = p1[0][0] - np.sin(ang) * l
                hy = p1[0][1] - np.cos(ang) * l
                lB = (lx,ly)
                rB = (rx,ry)
                head = (hx,hy)
                p1[0] = head
                p1[1] = lB
                p1[2] = rB
            # print(ang)
    elif color == 'black':
        for l, r in zip(lV,rV):
            printBoard()
            printPieces(pieceLoc)
            timeStep(1)
            if abs(l) > abs(r): #moving to the right
                r1 = (base * r) / (l - r)
                r2 = base + r1
                r3 = np.sqrt((base)**2 + (base/2 + r1)**2)
                ang = l / r2
                
                angAxis = np.arctan((p1[2][1] - p1[1][1]) / (p1[2][0] - p1[1][0]))
                cX = -r1 * np.cos(-angAxis) + p1[2][0]
                cY = r1 * np.sin(-angAxis) + p1[2][1]
                angh = abs(np.arctan((p1[0][1] - cY) / (p1[0][0] - cX)))
                # pygame.draw.circle(gameDisplay, (255,0,0), (cX,cY), 5, 0)
                # pygame.display.update()
                # timeStep(1)
                rX = cX + r1 * np.cos(ang + angAxis)
                rY = cY + r1 * np.sin(ang + angAxis)
                lX = cX + r2 * np.cos(ang + angAxis)
                lY = cY + r2 * np.sin(ang + angAxis)
                hX = cX + r3 * np.cos(ang + angh) 
                hY = cY + r3 * np.sin(ang + angh)
                p1[0] = (hX,hY)
                p1[1] = (lX,lY)
                p1[2] = (rX,rY)
            elif abs(l) < abs(r): #moving to the left
                r1 = (base * l) / (r-l)
                r2 = base + r1
                r3 = np.sqrt((base)**2 + (base/2 + r1)**2)
                ang = r / r2
                
                angAxis = np.arctan((p1[2][1] - p1[1][1]) / (p1[1][0] - p1[2][0]))
                cX = r1 * np.cos(angAxis) + p1[1][0]
                cY = -r1 * np.sin(angAxis) + p1[1][1]
                angh = abs(np.arctan((p1[0][1] - cY) / (cX - p1[0][0])))
                rX = cX - r2 * np.cos(ang + angAxis)
                rY = cY + r2 * np.sin(ang + angAxis)
                lX = cX - r1 * np.cos(ang + angAxis)
                lY = cY + r1 * np.sin(ang + angAxis)
                hX = cX - r3 * np.cos(ang + angh) 
                hY = cY + r3 * np.sin(ang + angh)
                
                p1[0] = (hX,hY)
                p1[1] = (lX,lY)
                p1[2] = (rX,rY)
            else: #moving forward/backward
                ang = np.arccos((p1[2][0]-p1[1][0]) / base)
                ang = ang if p1[2][1] < p1[1][1] else -1*ang #pos angle -> turning left
                lx = p1[1][0] - np.sin(ang) * l
                ly = p1[1][1] - np.cos(ang) * l
                rx = p1[2][0] - np.sin(ang) * r
                ry = p1[2][1] - np.cos(ang) * r
                hx = p1[0][0] - np.sin(ang) * l
                hy = p1[0][1] - np.cos(ang) * l
                lB = (lx,ly)
                rB = (rx,ry)
                head = (hx,hy)
                p1[0] = head
                p1[1] = lB
                p1[2] = rB
            # print(ang)
    printBoard()
    printPieces(pieceLoc)
    
    return ang



def chessSim():
    global size
    global gameDisplay
    pygame.init()
    game = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False
        
        while game:
            global size
            global gameDisplay
            printBoard()
            pieceLoc = []
            pieceLoc = setPieces(pieceLoc)               
            #hardcode start triangle on e2 and c2
            #hardcode move triangle on e2 --> [6,4] to [3,1]
            piece = [1,6] #start coord
            turn = 'black'
            loc = getTriPoints(piece, turn)
            for p in pieceLoc:
                if p == loc:
                    p1 = p
                    found = True
                    break
                else:
                    found = False
            if not found:
                print("Piece not found")
                pygame.quit()
                return
            
            #need to compute angle, distance, and direction
            
            #moveRobot(pieceLoc,p1,np.pi/4, 212,1)
            
            lV = []
            rV = []
            
            t = 5
            lV = [5]*t
            rV = [2]*t
            temp = [12]*t
            for a in temp:
                lV.append(a)
                rV.append(a)
            for a in range(10):
                lV.append(-5)
                rV.append(-2)
            
            # for a in range(t):
            #     lV.append(2)
            #     rV.append(5)
            # for a in range(t):
            #     lV.append(18)
            #     rV.append(18)
            # for a in range(t):
            #     lV.append(-2)
            #     rV.append(-5)
                
            moveWheels(lV,rV,pieceLoc,p1, turn)
            
            # piece = [6,2] #start coord
            # turn = 'white'
            # loc = getTriPoints(piece, turn)
            # for p in pieceLoc:
            #     if p == loc:
            #         p1 = p
            #         found = True
            #         break
            #     else:
            #         found = False
            # if not found:
            #     print("Piece not found")
            #     pygame.quit()
            #     return
            
            # moveWheels(lV,rV,pieceLoc,p1, turn)
            
            
            game = False
                
            
            
    pygame.quit() 
    




 
#run simulation if this file directly being called by terminal
if __name__ == '__main__' :
    chessSim()