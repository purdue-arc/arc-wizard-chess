#Movement
#Invoke-WebRequest -UseBasicParsing 192.168.2.2 -ContentType "text/plain" -Method POST -Body "Go"
Invoke-WebRequest -UseBasicParsing 192.168.2.2 -ContentType "text/plain" -Method POST -Body "Stop"


#ID Commands
#Invoke-WebRequest -UseBasicParsing 192.168.2.2 -ContentType "text/plain" -Method POST -Body "SetId pawnB1"
#Invoke-WebRequest -UseBasicParsing 192.168.2.2 -ContentType "text/plain" -Method POST -Body "GetId"
