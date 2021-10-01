# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 20:37:39 2021

@author: broat
"""                                                                             
import speech_recognition as sr  

HOUNDIFY_CLIENT_ID = "b1BYfHRMT5gMxWJfGjB5fQ=="
HOUNDIFY_CLIENT_KEY = "766ChPXbWST6WnK12EAhdBNCVpBBbPt1J2LuLRRwoj53N2Y7yquZmoX8Zf0kIFHfSGV4MJ2lkn21-ub7TnLCyQ=="


#---------------------------------------------------------------------------------------------------------------------
def replaceStringWithNum(inputString):
    outputNum = 0
    
    if inputString == "one":
        outputNum = 1
    elif inputString == "two":
        outputNum = 2
    elif inputString == "three":
        outputNum = 3
    elif inputString == "four":
        outputNum = 4
    elif inputString == "five":
        outputNum = 5
    elif inputString == "six":
        outputNum = 6
    elif inputString == "seven":
        outputNum = 7
    elif inputString == "eight":
        outputNum = 8
    return outputNum

def getStartAudio():
    # get audio from the microphone                                                                       
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Waiting for start: ")                                                                                   
        audio = r.listen(source)
    
    #translate audio file into string and split into components
    startCommand = r.recognize_houndify(audio, HOUNDIFY_CLIENT_ID, HOUNDIFY_CLIENT_KEY)
    splitStart = startCommand.split()
    print(splitStart)
    
    #check anywhere for the command "make move"
    if len(splitStart) == 0:
        getStartAudio()
    elif len(splitStart) > 0 and len(splitStart) < 1000:
        for i in range(len(splitStart)):
            if splitStart[i] == "make":
                if splitStart[i+1] == "move":             
                    return getMoveAudio()
    else:
        getStartAudio()

def getMoveAudio():
    # get audio from the microphone                                                                       
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Waiting for play: ")                                                                                   
        audio = r.listen(source)   

    #translate audio file into string and split into components
    inputCommand = r.recognize_houndify(audio, HOUNDIFY_CLIENT_ID, HOUNDIFY_CLIENT_KEY)
    splitCommand = inputCommand.split()
    
    #translate string numbers into usable integers
    if len(splitCommand) == 5:
        splitCommand[1] = str(replaceStringWithNum(splitCommand[1]))
        splitCommand[4] = str(replaceStringWithNum(splitCommand[4]))
    
    print(splitCommand)
    return splitCommand


#-----------------------------------------------------------------------------------------------------------------------
#initialize listening
gameOver = False
splitCommand = getStartAudio()

while gameOver != True:
    #error checking and location designations
    if len(splitCommand) != 5 or splitCommand[2].lower() != "target":
        print("Use the correct command: (start space) 'target' (end space)")
        splitCommand = getMoveAudio()
    elif len(splitCommand[0]) != 1 or len(splitCommand[1]) != 1 or len(splitCommand[3]) != 1 or len(splitCommand[4]) != 1 :
        print("Use correct location formatting: letter (a to g) + number (1 to 8)")
        splitCommand = getMoveAudio()
    else:
        gameOver = True
        startSpace = (splitCommand[0], splitCommand[1])
        endSpace = (splitCommand[3], splitCommand[4])
