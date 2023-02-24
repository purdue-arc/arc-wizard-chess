from machine import UART
from time import sleep, time

#Process HTTP Variables
userAgent = ""
contentType = ""
host = ""
connection = ""
messageType = ""

uart = UART(0, 115200)

def sendBasicAT(command, numResponses, logging):
    if logging == 1:
        print('SENDING DATA TO AT: ' + command + '\\r\\n')
    uart.write(command + '\r\n')
    for i in range(numResponses):
        while not(uart.any()):
            sleep(0.01)
        compiledInput = ""
        while uart.any():
            compiledInput += uart.readline().decode('utf-08')
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
        sendBasicAT(messageToSendBack, 1, 0)
        print("Replied with: " + messageToSendBack)
    except:
        print("Error Closing Connection: ")

def processPayload(payload, connectionId):
    try:
        if(payload[0:10]=="FIRMWARE:\n"):
            print("Firmware Update")
            print("New Firmware")
            print("------------")
            firmware = payload[10:]
            print(firmware)
            reply = "successful"
        else:
            print("The following payload was delivered from connection " + str(connectionId) + ":")
            print(payload)
            reply = input('Enter Reply Message: ') # replace hardcode value with function of what the message body was
        closeConnection(connectionId, reply)
    except:
        print("Error Processing Payload")
        
def processsHTTPMessage(message, connectionId):
    global userAgent
    global contentType
    global host
    global connection
    global messageType
    #print("INCOMING MESSAGE:\n" + message)
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
        

commandBeingProcessed = -1
openConnections = []
initializeESP01(0)
receivingBuffer = ""
while True:
    esp01Input = uart.readline()
    if (esp01Input is not None):
        receivingBuffer += esp01Input.decode('utf-08')
        if "\r\n" in receivingBuffer or "+IPD" in receivingBuffer:
            if(parseRuntimeResult(receivingBuffer)==1):
                #print(receivingBuffer, end="")
                receivingBuffer = ""