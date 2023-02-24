$code = 
"import math
import time
from machine import Pin
from time import sleep

def writeError(error, fileName):
    try:
        logFile = open(fileName, 'a')
        logFile.write(error)
        logFile.close()
    except Exception as e:
        print(str(e) + '\n')

def main():
    led = Pin(25, Pin.OUT)
    print('Running Main')
    if((time.time())%3==1):
        print('LED ON: ' + str((time.time())%2))
        led.on()
    else:
        led.off()
        print('LED OFF: ' + str((time.time())%2))
    time.sleep(0.1)

def initialize():
    print('Running Init')
    led = Pin(25, Pin.OUT)
    led.on()
    led.off()

def processMessage(message, fileName):
    print('message received')
    writeError('----\n', fileName)
    if message == 'Test_Message':
        return str(message + 'Yay6')
    elif message == 'Motors':
        return str('Moved Motors')
    else:
        return 'UndefinedMessage'

"

$maxStringLength = 30

Invoke-WebRequest -UseBasicParsing 192.168.2.3 -ContentType "text/plain" -Method POST -Body "FIRMWARE_CLEAR"
Start-Sleep -Milliseconds 100

while ($code) #While Code has not been displayed
{
    #Determine the length of the string that will be sent (as long as possible up to $maxStringLength)
    $segmentLength = ($maxStringLength,($code.Length) | Measure -Min).Minimum

    #Get the next segment of code and display the segment
    $segment = $code.Substring(0,$segmentLength)
    $messageBody = "FIRMWARE:`n" + $segment
    Invoke-WebRequest -UseBasicParsing 192.168.2.3 -ContentType "text/plain" -Method POST -Body $messageBody

    #Remove the displayed Segment from the code
    $code = $code.Remove(0, $segmentLength)
    Start-Sleep -Milliseconds 100
}

Invoke-WebRequest -UseBasicParsing 192.168.2.3 -ContentType "text/plain" -Method POST -Body "FIRMWARE_COMPLETE"