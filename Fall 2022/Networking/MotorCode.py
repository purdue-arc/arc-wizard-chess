import math
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
    #print('stop')
    motor1a.duty_u16(0)
    motor1b.duty_u16(0)
    motor1e.low()
    motor2a.duty_u16(0)
    motor2b.duty_u16(0)
    motor2e.low()
    writeError('Stopped Motors', errorFileName)
    
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