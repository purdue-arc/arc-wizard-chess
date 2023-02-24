$code = 
"import math
import time
from machine import Pin, ADC, PWM  
from time import sleep
import micropython
import utime

motor1a = PWM(Pin(18))
motor1b = PWM(Pin(17))
motor1e = Pin(16,Pin.OUT)
motor2a = PWM(Pin(13))
motor2b = PWM(Pin(14))
motor2e = Pin(15,Pin.OUT)
enca = Pin(0,Pin.IN, Pin.PULL_UP)
encb = Pin(1,Pin.IN, Pin.PULL_UP)
stopper = Pin(2,Pin.IN,Pin.PULL_UP)
potentiometer=ADC(28)
pot2 = ADC(27)

rot1 = 1181  

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
        led.on()
        print('LED OFF: ' + str((time.time())%2))
    time.sleep(0.1)  

def stop(errorFileName):
    writeError('Test1', errorFileName)
    #print('stop')
    motor1a.duty_u16(0)
    writeError('Test2', errorFileName)
    motor1b.duty_u16(0)
    writeError('Test3', errorFileName)
    motor1e.low()
    writeError('Test4', errorFileName)
    motor2a.duty_u16(0)
    writeError('Test5', errorFileName)
    motor2b.duty_u16(0)
    writeError('Test6', errorFileName)
    motor2e.low()
    writeError('Test7', errorFileName)
    
#Max value for duty cycle is 65535 which will send robot at max speed
def forward1(duty): #Right motor
    #print('forward')
    motor1a.duty_u16(duty)
    motor1b.duty_u16(0)
    motor1e.high()
    
def backward1(duty): #Left Motor
    print('backward')
    motor1a.duty_u16(0)
    motor1b.duty_u16(duty)
    motor1e.high()

def forward2(duty): #Left Motor

    motor2a.duty_u16(duty)
    #65535 = max duty cycle value
    motor2b.duty_u16(0)
    motor2e.high()
    
def backward2(duty): #Right Motor
    motor2a.duty_u16(0)
    motor2b.duty_u16(duty)
    motor2e.high()

def initialize():
    print('Running Init')
    led = Pin(25, Pin.OUT)
    led.on()
    led.off()
    
def blink():
    led = Pin(25, Pin.OUT)
    led.off()
    sleep(3)
    led.on()
    
def processMessage(message, fileName):
    print('message received')
    writeError('----\n', fileName)
    if message == 'Test_Message':
        return str(message + 'Yay6')
    elif message == 'Motors':
        return str('Moved Motors')
    elif message == 'Blink':
        blink()
        return str('Blinked')
    elif message == 'Go':
        forward1(30000)
        forward2(30000)
        return str('Successful')
    elif message == 'Stop':
        stop(fileName)
        return str('Successful')
    else:
        return 'UndefinedMessage'
"

$maxStringLength = 100

function consoleLogger
{
    process{Write-Host $_ -ForegroundColor yellow -BackgroundColor black}
}

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
    Write-Output $code.Length | consoleLogger
    Start-Sleep -Milliseconds 200 #This is necessary to allow for the ESP to switch back into "receiving mode"
}

Invoke-WebRequest -UseBasicParsing 192.168.2.3 -ContentType "text/plain" -Method POST -Body "FIRMWARE_COMPLETE"