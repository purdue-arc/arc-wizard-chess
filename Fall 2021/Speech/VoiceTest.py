# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 20:37:39 2021

@author: broat
"""                                                                             
import speech_recognition as sr  
import os
from wit import Wit

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ChessVoiceCredentials.json'
witKey = 'BNWXGM5MOPGWMVWKMKFANYBJVMHRHTV2'
client = Wit(witKey)
#---------------------------------------------------------------------------------------------------------------------

def getMoveAudio():
    tryMove = False
    while tryMove == False:
        input("Press enter to say your move\n")  
        
        # get audio from the microphone                                                                     
        recog = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:                                                                       
            print("Waiting for play: \n")  
            #audio = recog.adjust_for_ambient_noise(source, duration = 3)                                                                                   
            audio = recog.listen(source)   
    
        #translate audio file into string and split into components, or rerun if error
        try:
            inputCommand = recog.recognize_google_cloud(audio)
            tryMove = True
        except sr.UnknownValueError:
            print("Google Cloud Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech Recognition service; {0}".format(e))
        
    witReturn = client.message(inputCommand)
    if(len(witReturn) != 4):
        print("error reading values")
        print(inputCommand.split())
        getMoveAudio()
    
    moveList = []
    for i in range(0,3):
        moveList.append(witReturn['entities']['chess_position:chess_position'][i]['value'])
    
    
    startSpace = list(moveList[0].lower())
    endSpace = list(moveList[2].lower())
    
    return startSpace, endSpace


#-----------------------------------------------------------------------------------------------------------------------

