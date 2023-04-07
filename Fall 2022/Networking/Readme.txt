1) Flash boot code to robot with USB.  It must be named boot.py in the main folder of the pico filesystem
2) Add a logs folder ("logs" with out the quotes) to the filesystem of the pico
3) Reboot pico
4) Determine pico IP (arp -a or nslookup on cmd?)
5) upload main robot code over wifi (sendFirmware)
6) Run commands!