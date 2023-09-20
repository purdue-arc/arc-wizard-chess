# TODO:
# How to access log files (can't send whole file - too large?)
# How to display line with syntax error in main?

from machine import UART
from time import sleep, time
import sys
import os
from machine import Pin

led = Pin(25, Pin.OUT)
led.off()

#Process HTTP Variables
userAgent = ""
contentType = ""
host = ""
connection = ""
messageType = ""
firmwareFlashWaitingForRestart = 0
runMain = 1

#Error log file name
fileName = ""

def writeError(error, fileName):
    try:
        logFile = open(fileName, "a")
        logFile.write(error)
        logFile.close()
    except Exception as e:
        print(str(e) + "\n")

def getMaxLogId():
    logId = 0
    while 1 == 1:
        try:
            os.stat("logs/log" + str(logId) + ".txt")
        except Exception as e:
            return logId - 1 #Return the last id that does not throw	 an error
        logId = logId + 1

def sendBasicAT(command, numResponses, logging):
    if logging == 1:
        print('SENDING DATA TO AT: ' + command + '\\r\\n')
    uart.write(command + '\r\n')
    for i in range(numResponses):
        while not(uart.any()):
            sleep(0.01)
        compiledInput = ""
        while uart.any():
            try:
                compiledInput += uart.readline().decode('utf-08')
            except Exception as e:
                #print(compiledInput)
                #print("Waiting for more data from ESP01")
                pass
            sleep(0.01)
        if logging == 1:
            print("Serial Input: " + compiledInput)

def sendHTTPReplyAT(command, numResponses, logging):
    if logging == 1:
        print('SENDING DATA TO AT: ' + command + '\\r\\n')
    uart.write(command + '\r\n')
    for i in range(numResponses):
        while not(uart.any()):
            sleep(0.01)
        compiledInput = ""
        while uart.any() or compiledInput.find("SEND OK") == -1:
            try:
                compiledInput += uart.readline().decode('utf-08')
            except Exception as e:
                #print(compiledInput)
                #print("Waiting for more data from ESP01")
                pass
            sleep(0.01)
        if logging == 1:
            print("Serial Input: " + compiledInput)

def initializeESP01(connectWifi):
    sendBasicAT('AT', 1, 1)
    sendBasicAT('AT+GMR', 1, 1)
    sendBasicAT('AT+CWMODE=1', 1, 1)
    sendBasicAT('AT+CIPSTATUS', 1, 1)
    
    if connectWifi == 1:
        sendBasicAT('AT+CWQAP', 1, 1)
        sendBasicAT('AT+CWJAP="wizardschess","wizardschess"', 4, 1)
    sendBasicAT('AT+CIPMUX=1',1, 1)
    sendBasicAT('AT+CIPSERVER=1,80',1, 1)

def closeConnection(connectionId, messageToSendBack):
    try:
        stringsToSend = ['HTTP/1.1 200',
                         'Content-Type: text/html',
                         'Content-Length: ' + str(len(messageToSendBack)+2),
                         'Connection: close',
                         '']
        for stringToSend in stringsToSend:
            sendBasicAT('AT+CIPSEND=' + str(connectionId) + ','+ str(len(stringToSend)+2), 1, 0)
            sendBasicAT(stringToSend, 2, 0)
        sendBasicAT('AT+CIPSEND=' + str(connectionId) + ','+ str(len(messageToSendBack)+2), 1, 0)
        sendHTTPReplyAT(messageToSendBack, 1, 0)#Special reply because 'SEND OK' will sometimes be delayed from main message
        print("Replied with: " + messageToSendBack)
    except Exception as e:
        print("Error Closing Connection: ")
        print(str(e))

def appendFirmware(firmware):
    global firmwareFlashWaitingForRestart
    global fileName
    try:
        #print("attempting to write: " + firmware)
        try:
            firmwareFile = open("main.py", "a")
            firmwareFile.write(firmware)
            #print("Wrote firmware")
            firmwareFile.close()
        except Exception as e:
            print("File does not exist")
            print(str(e))
        firmwareFile = open("main.py", "r")
        #print("File Contents: " + str(firmwareFile.readlines()))
        firmwareFile.close()
    except Exception as e:
        print("Error flashing to main.py")
        print(str(e))
        writeError(str(e) + "\n", fileName)

def clearFirmware():
    try:
        try:
            firmwareFile = open("main.py", "w")
            firmwareFile.write("")
            print("Cleared main.py")
            firmwareFile.close()
        except:
            print("File does not exist")
            global fileName
            writeError("File does not exist", fileName)
    except Exception as e:
        print("Error clearing main.py")
        print(str(e))
        global fileName
        writeError("Error clearing main.py", fileName)
        writeError(str(e) + "\n", fileName)

def processPayload(payload, connectionId):
    global fileName
    global runMain
    try:
        if(payload[0:10]=="FIRMWARE:\n"):
            #print("Firmware Update")
            #print("New Firmware")
            #print("------------")
            firmware = payload[10:]
            #print(firmware)
            try:
                appendFirmware(firmware)
            except Exception as e:
                print(str(e))
            reply = "successful"
        elif(payload[0:14]=="FIRMWARE_CLEAR"):
            runMain = 0
            clearFirmware()
            reply = "successful"
        elif(payload[0:17]=="FIRMWARE_COMPLETE"):
            global firmwareFlashWaitingForRestart
            print("RESTART NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            firmwareFlashWaitingForRestart = 1
            reply = "successful"
        elif(payload[0:12]=="LOG_RETREIVE"):
            print('logRetreive')
            try:
                logId = payload.split(' ')[1]
                fileName = "logs/log" + str(logId) + ".txt"
                try:
                    print(str(fileName))
                    logReadingFile = open(fileName, "r")
                    reply = logReadingFile.read()
                    logReadingFile.close()
                    print(reply)
                except Exception as e:
                    print(str(e) + "\n")
                    writeError(str(e) + "\n", fileName)
                    reply = "Failed to Retrieve Log"
            except:
                logCount = getMaxLogId() #If format was wrong or like 'LOG_RETREIVE', return the log count
                reply = "Maximum Log Id: " + str(logCount)
        elif(payload[0:9] == "LOG_ERASE"):
            print("clearing logs")
            files = os.listdir("logs")
            for f in files:
                os.remove('logs/' + f)
            reply = 'success'
            print("success")
        else:
            print("The following payload was delivered from connection " + str(connectionId) + ":")
            print(payload)
            try:
                global main
                reply = main.processMessage(payload, fileName)
            except Exception as e:
                print(str(e))
                writeError(str(e) + "\n", fileName)
            print('test')
            if reply is None:
                reply = "Message Not Processed.  Check main.py for a 'processMessage' function and ensure that a string is being returned by processMessage."
        closeConnection(connectionId, reply)
    except Exception as e:
        writeError("Error Processing Payload:", fileName)
        writeError(str(e), fileName)
        
        print("Error Processing Payload:")
        print(str(e))
        
def processsHTTPMessage(message, connectionId):
    global userAgent
    global contentType
    global host
    global connection
    global messageType
    print("INCOMING MESSAGE:\n" + message)
    lines = message.split('\r\n')
    if messageType == "POST":
        processPayload(message, connectionId)
        messageType = ""
    else:
        for line in lines:
            try:
                #print("Processing HTTP Line: " + line)
                if 'POST' in line:
                    userAgent = ""
                    contentType = ""
                    host = ""
                    connection = ""
                    messageType = "POST"
                elif 'GET' in line:
                    userAgent = ""
                    contentType = ""
                    host = ""
                    connection = ""
                    messageType = "GET"
                elif "User-Agent: " in line:
                    userAgent = line.split(": ")[1].replace("\n","")
                elif "Content-Type: " in line:
                    contentType = line.split(": ")[1].replace("\n","")
                elif "Host: " in line:
                    host = line.split(": ")[1].replace("\n","")
                elif "Connection: " in line:
                    connection = line.split(": ")[1].replace("\n","")
            except:
                print('Error Processing Above Line')
def parseRuntimeResult(inputString):
    #Handle Connection Opening
    if ",CONNECT" in inputString:
        #Add the integer part of the input to openConnections
        if int(inputString[0:inputString.index(',')]) not in openConnections:
            openConnections.append(int(inputString[0:inputString.index(',')]))
            print("Opened Connections: " + str(openConnections))
        return 1
    #Handle Connection Closing
    elif ",CLOSED" in inputString:
        #Add the integer part of the input to openConnections
        print(inputString)
        if int(inputString[0:inputString.index(',')]) in openConnections:
            openConnections.remove(int(inputString[0:inputString.index(',')]))
            print("Opened Connections: " + str(openConnections))
        return 1
    elif "+IPD" in inputString:
        try:
            inputString = "+IPD" + inputString.split("+IPD")[-1]
            connectionId = int(inputString.split(',')[1])
            targetMessageLength = int(inputString.split(',')[2].split(':')[0])
            currentMessageLength = len(inputString)-inputString.index(":")-1
        
            if(targetMessageLength != currentMessageLength):
                #keep waiting for the message to be complete
                #print("[" + str(currentMessageLength) + "/" + str(targetMessageLength) + "]")
                #print(inputString)
                return 0
            else:
                messageBody = inputString.replace(inputString.split(':')[0] + ':', '', 1)
                processsHTTPMessage(messageBody, connectionId)
            #commandBeingProcessed = int(inputString.split(',')[1])
            #print("Processing For Connection: " + str(commandBeingProcessed))
            #userAgent = ""
            #contentType = ""
            #host = ""
            #connection = ""
                return 1
        except:
            return 0 #Keep waiting for the message to send
    
    elif "\r\n" == inputString:
        print("\n")
        return 1
    else:
        print("Unknown Input: " + inputString)
        return 1
    
#-------------------------------------------------
#-----------------MAIN----------------------------
#-------------------------------------------------
logNumber = 0
fileName = "logs/log.txt"
while (fileName == "logs/log.txt"):
    try:
        os.stat("logs/log" + str(logNumber) + ".txt")
    except Exception as e:
        fileName = "logs/log" + str(logNumber) + ".txt"
    logNumber += 1
logNumber -= 1
print("LogNumber: " + str(logNumber))
writeError("Log: " + str(logNumber) + "\n", fileName)
writeError("----\n", fileName)

runMain = 0
try:
    import main
    runMain = 1
except Exception as e:
    print("Error importing main")
    print(type(e), e)
    writeError("Error importing main.py: ", fileName)
    writeError(str(e) + "\n", fileName)
   
uart = UART(0, 115200)
while uart.any():
    uart.read()
led = Pin(25, Pin.OUT)
led.off()
initializeESP01(1) #Change to one to connect to wifi
try:
    main.initialize()
except Exception as e:
    print("Error running main.initialize")
    writeError(str(e) + "\n", fileName)
led.on()
commandBeingProcessed = -1
openConnections = []
receivingBuffer = ""
while True:
    esp01Input = uart.readline()
    if (esp01Input is not None):
        #print("received info")
        receivingBuffer += esp01Input.decode('utf-08')
        if "\r\n" in receivingBuffer:
            
            #Parse the buffer and see if it was successfully parsed.
            if(parseRuntimeResult(receivingBuffer)==1):
                #print("Clearing" + receivingBuffer)
                receivingBuffer = ""
        if "+IPD" in receivingBuffer:
            #connection opened. Pause actions till connection is handled
            while receivingBuffer != "":
                esp01Input = uart.readline()
                if (esp01Input is not None):
                    receivingBuffer += esp01Input.decode('utf-08')
                if(parseRuntimeResult(receivingBuffer)==1):
                    try:
                        openConnections.remove(int(receivingBuffer.split(',')[1])) # Close the connection after message has been processed (if needed)
                    except Exception as e:
                        pass #This isn't an issue because the connection has already been closed
                    receivingBuffer = ""
    else:
        if len(openConnections) == 0:
            try:
                if(runMain == 1):
                    main.main()
                    pass
            except Exception as e:
                print("Error running main.main")
                print(str(e))
                runMain = 0
                pass
            if(firmwareFlashWaitingForRestart == 1):
                firmwareFlashWaitingForRestart = 0
                print("resetting")
                machine.reset()
        else:
            pass
            #print(openConnections)
