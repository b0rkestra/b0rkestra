#!/usr/bin/env python

from OSC import OSCServer
import sys
from time import sleep
import threading
import RPi.GPIO as GPIO
from RPIO import PWM

server = OSCServer( ("192.168.1.11", 7110) )
server.timeout = 0
run = True

GPIO.setmode(GPIO.BCM)

GPIO.setup(2,  GPIO.OUT) #1 bank 1
GPIO.output(2, GPIO.HIGH)
GPIO.setup(3,  GPIO.OUT) #2 bank 1
GPIO.output(3, GPIO.HIGH)
GPIO.setup(4,  GPIO.OUT) #3 bank 1
GPIO.output(4, GPIO.HIGH)
GPIO.setup(14, GPIO.OUT) #4 bank 1
GPIO.output(14, GPIO.HIGH)
GPIO.setup(15, GPIO.OUT) #5 bank 1
GPIO.output(15, GPIO.HIGH)
GPIO.setup(18, GPIO.OUT) #6 bank 1
GPIO.output(18, GPIO.HIGH)

GPIO.setup(17, GPIO.OUT) #16 bank 1
GPIO.output(17, GPIO.HIGH)
GPIO.setup(27, GPIO.OUT) #15 bank 1
GPIO.output(27, GPIO.HIGH)
GPIO.setup(22, GPIO.OUT) #14 bank 1
GPIO.output(22, GPIO.HIGH)
GPIO.setup(23, GPIO.OUT) #13 bank 1
GPIO.output(23, GPIO.HIGH)
GPIO.setup(24, GPIO.OUT) #12 bank 1
GPIO.output(24, GPIO.HIGH)
GPIO.setup(25, GPIO.OUT) #11 bank 1
GPIO.output(25, GPIO.HIGH)



GPIO.setup(10, GPIO.OUT) #1 bank 2
GPIO.output(10, GPIO.HIGH)
GPIO.setup(9,  GPIO.OUT) #2 bank 2
GPIO.output(9, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT) #3 bank 2
GPIO.output(11, GPIO.HIGH)
GPIO.setup(8,  GPIO.OUT) #4 bank 2
GPIO.output(8, GPIO.HIGH)
GPIO.setup(7,  GPIO.OUT) #5 bank 2
GPIO.output(7, GPIO.HIGH)
GPIO.setup(5,  GPIO.OUT) #6 bank 2
GPIO.output(5, GPIO.HIGH)

GPIO.setup(6,  GPIO.OUT) #16 bank 2
GPIO.output(6, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT) #15 bank 2
GPIO.output(13, GPIO.HIGH)
GPIO.setup(19, GPIO.OUT) #14 bank 2
GPIO.output(19, GPIO.HIGH)
GPIO.setup(26, GPIO.OUT) #13 bank 2
GPIO.output(26, GPIO.HIGH)
GPIO.setup(12, GPIO.OUT) #12 bank 2
GPIO.output(12, GPIO.HIGH)
GPIO.setup(16, GPIO.OUT) #11 bank 2
GPIO.output(16, GPIO.HIGH)


"""
PWM.setup()
PWM.init_channel(0)
"""




class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)


def hit(gpio, pin, vel=100):

    sleeptime = (0.06/127.0)*vel
    gpio.output(pin,False)
    sleep(sleeptime)
    gpio.output(pin,True)
    return



def note(value, pin):
    #PWM.setup()
    #PWM.clear_channel_gpio(0, pin)
    print "siren", value
    #TODO - Add mapping between midi value and PWM speed

    PWM.add_channel_pulse(0, pin, 0, value)
    sleep(0.5)
    PWM.clear_channel_gpio(0, pin)


# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)




def sunguitar_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    print ("Now do something with", user,args) 
    
    print(args)
    pin = None
    
    if(args[0]==60):   # E1
        pin = 17     
    elif(args[0]==61): # F1
        pin = 2
    elif(args[0]==62): # F#1
        pin = 6   
    elif(args[0]==63): # G1
        pin = 10
    elif(args[0]==64): # G#1
        pin = 27
    elif(args[0]==65): # A1
        pin = 3
    elif(args[0]==66): # A#1
        pin = 13
    elif(args[0]==67): # B1
        pin = 9
    elif(args[0]==68): # C2
        pin = 22
    elif(args[0]==69): # C#2
        pin = 4
    elif(args[0]==70): # D2
        pin = 19
    elif(args[0]==71): # D#2
        pin = 11
    elif(args[0]==72): # E2
        pin = 23
    elif(args[0]==73): # F2
        pin = 14
    elif(args[0]==74): # F#2
        pin = 26
    elif(args[0]==75): # G2
        pin = 8   
    elif(args[0]==76): # G#2
        pin = 24
    elif(args[0]==77): # A2
        pin = 15
    elif(args[0]==78): # A#2
        pin = 12
    elif(args[0]==79): # B2
        pin = 7
    elif(args[0]==80): # C3
        pin = 19
    elif(args[0]==81): # C#3
        pin = 18
    elif(args[0]==82): # D3
        pin = 16
    elif(args[0]==83): # D#3
        pin = 5




    vel = args[1]
    print('vel',vel)
    if pin != None:
        FuncThread(hit, GPIO, pin,vel).start()
    else:
        print "note not in range"



def drum_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    print ("Now do something with", user,args) 
    
    print(args)
    pin =3
    
    if(args[0]==60):
        pin = 3     
    elif(args[0]==61):
        pin = 5
    elif(args[0]==62):
        pin =7  
    
    FuncThread(hit, GPIO, pin).start()


def siren_callback(path, tags, args, source):
    user = ''.join(path.split("/"))
    pin = 12
    FuncThread(note, args[0], pin).start()


def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

server.addMsgHandler( "/drums/1", drum_callback )
server.addMsgHandler( "/sunguitar/1", sunguitar_callback )
server.addMsgHandler( "/siren/1", siren_callback)
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

GPIO.cleanup() 
PWM.cleanup()
server.close()

print('fin')
