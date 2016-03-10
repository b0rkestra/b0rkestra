#!/usr/bin/env python3

import socket
import fcntl
import struct
import math
import spidev

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

#Need this as rasberry pi is fuck ass backward
def ReverseBits(byte):
    byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
    byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
    byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
    return byte

def ReverseBitsInSet(byteset):

    yourmum = [0x00,0x00,0x00,0x00,0x00,0x00]
    for x in range(0, 6):
        yourmum[x] = ReverseBits(byteset[x])
    return yourmum  


server = OSCServer( ('0.0.0.0', 7110) )
server.timeout = 0
run = True

GPIO.setmode(GPIO.BOARD)  


RSTPIN1 = 3 
RSTPIN2 = 5
RSTPIN3 = 7    
RSTPIN4 = 11  
bNoteOff = False



GPIO.setup(RSTPIN1, GPIO.OUT)
GPIO.setup(RSTPIN2, GPIO.OUT)
GPIO.setup(RSTPIN3, GPIO.OUT)
GPIO.setup(RSTPIN4, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode=0b00
#spi.max_speed_hz = 500000
spi.cshigh = True


#make all off
def makeOff(pin):
    GPIO.output(pin,True)
    spi.xfer2([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    GPIO.output(pin,False)


#makeOff(RSTPIN4)
#makeOff(RSTPIN3)
#makeOff(RSTPIN2)
#makeOff(RSTPIN1)

class FuncThread(threading.Thread):
    def __init__(self, target, *args):  
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)


def note(gpio, args):

 #note decides which pot we set, need to build 48 bits for clocking in. 
    # if you and with 0xC0 then it 'no note'
    # just and with 0x3F if we want a note. 

    set1 = genEmptyBytes()
    set2 = genEmptyBytes()
    set3 = genEmptyBytes()
    set4 = genEmptyBytes()
    
    byteset = set1
    offset = 48
    setpin = RSTPIN1

    print(args[0])

    #first 6 notes
    if((args[0] >= 48) and (args[0] <= 53)):
        byteset = set1
        offset = 48
        setpin = RSTPIN1

    elif((args[0] >= 54) and (args[0] <= 59)):
        byteset = set2
        offset = 54
        setpin = RSTPIN2


    elif((args[0] >= 60) and (args[0]<= 65)):
        byteset = set3
        offset = 60
        setpin = RSTPIN3


    elif((args[0] >= 66) and (args[0] <= 71)):
        byteset = set4
        offset = 66        
        setpin = RSTPIN4

    else: return

    byteset[args[0] - offset] = setByte(byteset[args[0] - offset], args[1])
    vel = args[1]

    if(vel!=0):
        GPIO.output(setpin,True)
        to_send = ReverseBitsInSet(byteset)
        print(setpin, to_send)
        resp = spi.xfer2(to_send)

        GPIO.output(setpin,False)
        
    if(False ==bNoteOff):
        sleep(0.1) #option now is to have note off. Might be better. 

        GPIO.output(setpin,True)

        resp = spi.xfer2(genOffBytes())
        
        GPIO.output(setpin,False)

    elif(vel==0):
        GPIO.output(setpin,True)    
        resp = spi.xfer2(genOffBytes())     
        GPIO.output(setpin,False)




    '''
    #The code below is basically fine. excpet its not. no idea why. fucking python. 


    print(setpin, byteset,ReverseBitsInSet(byteset), [ReverseBits(0x3F), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00)])

    GPIO.output(3,True)
    to_send = [ReverseBits(0x3F), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00)]

    #spi.xfer2(ReverseBitsInSet(byteset))

    what =spi.xfer2(to_send)
    #GPIO.output(setpin,False)


    #all a bit shit this, need to use note offs to stop it... butttttt.. for now...
    sleep(0.1)
    #GPIO.output(setpin,True)
    to_send = [ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00)]

    resp = spi.xfer2(to_send)    
    GPIO.output(3   ,False)
    '''


    return

def genEmptyBytes():
    byte = 0xC0
    bytes = [byte, byte, byte, byte, byte, byte];
    return bytes;

def genOffBytes():
    bytes = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00];
    return bytes;


def setByte(byte, notevel):
    sixtyfourbase = math.trunc((notevel/127)*64)
    #byte = byte & 0x3F not do vel for now
    byte = 0x3F
    return byte;


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
    print('rx',path,tags,args)
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    
   

    FuncThread(note, GPIO, args).start()


    

def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

def dummy_callback(path, tags, args, source):
    pass

server.addMsgHandler( "/tubulum/1", user_callback )

server.addMsgHandler( "/drums/1", dummy_callback )
server.addMsgHandler( "/racketguitar/1", dummy_callback )
server.addMsgHandler( "/sunguitar/1", dummy_callback )

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
    sleep(0.005)
    # call user script
    each_frame()


server.close()







