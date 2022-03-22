# Follow the tutorial from: https://circuitdigest.com/microcontroller-projects/interfacing-esp8266-01-wifi-module-with-raspberry-pi-pico


from machine import UART, Pin
import time
from esp8266 import ESP8266
print("1")

ssid = "wizardschess"
pwd = "wizardschess"


esp01 = ESP8266(baudRate=115200)

print("2")

print("StartUP",esp01.startUP())
#print("ReStart",esp01.reStart())
#print("StartUP",esp01.startUP())
print("Echo-Off",esp01.echoING())

esp8266_at_ver = None

esp8266_at_var = esp01.getVersion()
if(esp8266_at_var != None):
    print(esp8266_at_var)
else:
    print("No version - probably not loaded")

print("Setting WiFi Mode")
esp01.setCurrentWiFiMode()


print("Attempting to connect")
while(1):
    if "WIFI CONNECTED" in esp01.connectWiFi(ssid, pwd):
        print("ESP8266 connected")
        break;
    else:
        print(".")
        time.sleep(2)
   
   
time.sleep(1)
'''
Going to do HTTP Get Operation with www.httpbin.org/ip, It return the IP address of the connected device
'''
#httpCode, httpRes = esp01.doHttpGet("www.httpbin.org","/ip","RaspberryPi-Pico", port=80)
#print("------------- www.httpbin.org/ip Get Operation Result -----------------------")
#print("HTTP Code:",httpCode)
#print("HTTP Response:",httpRes)
#print("-----------------------------------------------------------------------------\r\n\r\n")

while (1):
    print('Waiting')
    time.sleep(10)
