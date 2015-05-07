#!/usr/bin/env python3

import socket
import fcntl
import struct

from OSC import OSCServer
import sys
from time import sleep
import threading
import RPi.GPIO as GPIO

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

#ipaddress = get_ip_address('eth0')

server = OSCServer( ('0.0.0.0', 7110) )

#server = OSCServer( ("192.168.1.255", 7110) )
server.timeout = 0
run = True


RSTPIN1 = 11;
CLKPIN = 12;
DATAPIN = 13    

GPIO.setmode(GPIO.BOARD)  

#setup clock
#GPIO.setup(CLKPIN,GPIO.ALT0)
#GPIO.setclock(CLKPIN,64000)

GPIO.setup(RSTPIN1, GPIO.OUT)
GPIO.setup(CLKPIN, GPIO.OUT)
GPIO.setup(DATAPIN, GPIO.OUT)





class FuncThread(threading.Thread):
    def __init__(self, target, *args):  
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)


def note(gpio, pin, vel,onval):

    offval = False
    if onval == False:
        offval = True

    sleeptime = (0.07/127)*vel;
    print(vel,sleeptime)
    gpio.output(pin,onval)
    sleep(sleeptime)
    gpio.output(pin,offval)
    return



# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

def user_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    print ("Now do something with", user,args) 
    
    print(args)

    #note decides which pot we set, need to build 48 bits for clocking in. 




    
    if(args[0]==60):
        pin = 3
        onval=True

    elif(args[0]==61):
        pin = 5
        onval=True

    elif(args[0]==62):
        pin =7
        onval=True

    elif(args[0]==63):
        pin = 11
        onval=False   

    elif(args[0]==64):
        pin = 13
        onval=False

    elif(args[0]==65):
        pin = 15
        onval=False


    vel = args[1]
    print(vel)

    FuncThread(note, GPIO, pin,vel,onval).start()
    
    #GPIO.output(3,True)
    #sleep(0.06)
    #GPIO.output(3,False)


def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

server.addMsgHandler( "/tubulum/1", user_callback )
server.addMsgHandler( "/quit", quit_callback )

# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()

# simulate a "game engine"
while run:
    # do the game stuff:
    sleep(0.01)
    # call user script
    each_frame()


server.close()







