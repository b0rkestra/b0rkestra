#!/usr/bin/env python

from OSC import OSCServer
import sys
from time import sleep
import threading
import RPi.GPIO as GPIO
from RPIO import PWM
import socket


# Get the ip address. (source: http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib)

ip_address = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
ip_address = "0.0.0.0"
print ip_address
server = OSCServer( (ip_address, 7110) )
server.timeout = 0
run = True

GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)

GPIO.setup(3,  GPIO.OUT) #1 bank 1
GPIO.output(3,  GPIO.LOW) 
GPIO.setup(5,  GPIO.OUT) #1 bank 1
GPIO.output(5,  GPIO.LOW)
GPIO.setup(7,  GPIO.OUT) #1 bank 1
GPIO.output(7,  GPIO.LOW)
GPIO.setup(11,  GPIO.OUT) #1 bank 1
GPIO.output(11,  GPIO.LOW)
GPIO.setup(13,  GPIO.OUT) #1 bank 1
GPIO.output(13,  GPIO.LOW)
GPIO.setup(15,  GPIO.OUT) #1 bank 1
GPIO.output(15,  GPIO.LOW)

GPIO.setup(8,  GPIO.OUT) #1 bank 2
GPIO.output(8,  GPIO.LOW)
GPIO.setup(10,  GPIO.OUT) #1 bank 2
GPIO.output(10,  GPIO.LOW)
GPIO.setup(12,  GPIO.OUT) #1 bank 2
GPIO.output(12,  GPIO.LOW)
GPIO.setup(16,  GPIO.OUT) #1 bank 2
GPIO.output(16,  GPIO.LOW)
GPIO.setup(18,  GPIO.OUT) #1 bank 2
GPIO.output(18,  GPIO.LOW)
GPIO.setup(22,  GPIO.OUT) #1 bank 2
GPIO.output(22,  GPIO.LOW)

GPIO.setup(19,  GPIO.OUT) #1 bank 3
GPIO.output(19,  GPIO.LOW)
GPIO.setup(21,  GPIO.OUT) #1 bank 3
GPIO.output(21,  GPIO.LOW)
GPIO.setup(23,  GPIO.OUT) #1 bank 3
GPIO.output(23,  GPIO.LOW)
GPIO.setup(29,  GPIO.OUT) #1 bank 3
GPIO.output(29,  GPIO.LOW)
GPIO.setup(33,  GPIO.OUT) #1 bank 3
GPIO.output(33,  GPIO.LOW)
GPIO.setup(35,  GPIO.OUT) #1 bank 3
GPIO.output(35,  GPIO.LOW)

GPIO.setup(24,  GPIO.OUT) #1 bank 3
GPIO.output(24,  GPIO.LOW)
GPIO.setup(26,  GPIO.OUT) #1 bank 3
GPIO.output(26,  GPIO.LOW)
GPIO.setup(32,  GPIO.OUT) #1 bank 3
GPIO.output(32,  GPIO.LOW)
GPIO.setup(36,  GPIO.OUT) #1 bank 3
GPIO.output(36,  GPIO.LOW)
GPIO.setup(38,  GPIO.OUT) #1 bank 3
GPIO.output(38,  GPIO.LOW)
GPIO.setup(40,  GPIO.OUT) #1 bank 3
GPIO.output(40,  GPIO.LOW)



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
    sleeptime = 0.04
    gpio.output(pin,True)
    sleep(sleeptime)
    gpio.output(pin,False)
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
    args[0] = args[0];
    if(args[0]==28):   # E1
        pin = 3     
    elif(args[0]==29): # F1
        pin = 5
    elif(args[0]==30): # F#1
        pin = 7   
    elif(args[0]==31): # G1
        pin = 11
    elif(args[0]==32): # G#1
        pin = 13
    elif(args[0]==33): # A1
        pin = 15
    elif(args[0]==34): # A#1
        pin = 8
    elif(args[0]==35): # B1
        pin = 10
    elif(args[0]==36): # C2
        pin = 12
    elif(args[0]==37): # C#2
        pin = 16
    elif(args[0]==38): # D2
        pin = 18
    elif(args[0]==39): # D#2
        pin = 22
    elif(args[0]==40): # E2
        pin = 19
    elif(args[0]==41): # F2
        pin = 21
    elif(args[0]==42): # F#2
        pin = 23
    elif(args[0]==43): # G2
        pin = 29  
    elif(args[0]==44): # G#2
        pin = 31
    elif(args[0]==45): # A2
        pin = 33
    elif(args[0]==46): # A#2
        pin = 24
    elif(args[0]==47): # B2
        pin = 26
    elif(args[0]==48): # C3
        pin = 32
    elif(args[0]==49): # C#3
        pin = 36
    elif(args[0]==50): # D3
        pin = 38
    elif(args[0]==51): # D#3
        pin = 40




    vel = args[1]
    print('vel',vel)
    if vel ==0:
        return
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

def dummy_callback(path, tags, args, source):
    pass

server.addMsgHandler( "/drums/1", dummy_callback )
server.addMsgHandler( "/sunguitar/1", sunguitar_callback )
server.addMsgHandler( "/siren/1", dummy_callback)
server.addMsgHandler( "/tubulum/1", dummy_callback)
server.addMsgHandler( "/racketguitar/1", dummy_callback)
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






#GPIO.setup(2,  GPIO.OUT) #1 bank 1
#GPIO.output(2, GPIO.LOW)
#GPIO.setup(3,  GPIO.OUT) #2 bank 1
#GPIO.output(3, GPIO.LOW)
#GPIO.setup(4,  GPIO.OUT) #3 bank 1
#GPIO.output(4, GPIO.LOW)
#GPIO.setup(14, GPIO.OUT) #4 bank 1
#GPIO.output(14, GPIO.LOW)
#GPIO.setup(15, GPIO.OUT) #5 bank 1
#GPIO.output(15, GPIO.LOW)
#GPIO.setup(18, GPIO.OUT) #6 bank 1
#GPIO.output(18, GPIO.LOW)

#GPIO.setup(17, GPIO.OUT) #16 bank 1
#GPIO.output(17, GPIO.LOW)
#GPIO.setup(27, GPIO.OUT) #15 bank 1
#GPIO.output(27, GPIO.LOW)
#GPIO.setup(22, GPIO.OUT) #14 bank 1
#GPIO.output(22, GPIO.LOW)
#GPIO.setup(23, GPIO.OUT) #13 bank 1
#GPIO.output(23, GPIO.LOW)
#GPIO.setup(24, GPIO.OUT) #12 bank 1
#GPIO.output(24, GPIO.LOW)
#GPIO.setup(25, GPIO.OUT) #11 bank 1
#GPIO.output(25, GPIO.LOW)



#GPIO.setup(10, GPIO.OUT) #1 bank 2
#GPIO.output(10, GPIO.LOW)
#GPIO.setup(9,  GPIO.OUT) #2 bank 2
#GPIO.output(9, GPIO.LOW)
#GPIO.setup(11, GPIO.OUT) #3 bank 2
#GPIO.output(11, GPIO.LOW)
#GPIO.setup(8,  GPIO.OUT) #4 bank 2
#GPIO.output(8, GPIO.LOW)
#GPIO.setup(7,  GPIO.OUT) #5 bank 2
#GPIO.output(7, GPIO.LOW)
#GPIO.setup(5,  GPIO.OUT) #6 bank 2
#GPIO.output(5, GPIO.LOW)

#GPIO.setup(6,  GPIO.OUT) #16 bank 2
#GPIO.output(6, GPIO.LOW)
#GPIO.setup(13, GPIO.OUT) #15 bank 2
#GPIO.output(13, GPIO.LOW)
#GPIO.setup(19, GPIO.OUT) #14 bank 2
#GPIO.output(19, GPIO.LOW)
#GPIO.setup(26, GPIO.OUT) #13 bank 2
#GPIO.output(26, GPIO.LOW)
#GPIO.setup(12, GPIO.OUT) #12 bank 2
#GPIO.output(12, GPIO.LOW)
#GPIO.setup(16, GPIO.OUT) #11 bank 2
#GPIO.output(16, GPIO.LOW)





 #if(args[0]==28):   # E1
 #       pin = 17
 #   elif(args[0]==29): # F1
 #       pin = 2
 #   elif(args[0]==30): # F#1
 #       pin = 6
 #   elif(args[0]==31): # G1
 #       pin = 10
 #   elif(args[0]==32): # G#1
 #       pin = 27
  #  elif(args[0]==33): # A1
   #     pin = 3
 #   elif(args[0]==34): # A#1
 #       pin = 13
 #   elif(args[0]==35): # B1
 #       pin = 9
 #   elif(args[0]==36): # C2
 #       pin = 22
 #   elif(args[0]==37): # C#2
 #       pin = 4
  #  elif(args[0]==38): # D2
   #     pin = 19
    #elif(args[0]==39): # D#2
 #       pin = 11
#    elif(args[0]==40): # E2
#        pin = 23
 #   elif(args[0]==41): # F2
 #       pin = 14
 #   elif(args[0]==42): # F#2
 #       pin = 26
 #   elif(args[0]==43): # G2
 #       pin = 8
 #   elif(args[0]==44): # G#2
 #       pin = 24
 #   elif(args[0]==45): # A2
 #       pin = 15
 #   elif(args[0]==46): # A#2
 #       pin = 12
 #   elif(args[0]==47): # B2#
#	pin = 7
#    elif(args[0]==48): # C3
#        pin = 25
#    elif(args[0]==49): # C#3
#        pin = 18
#    elif(args[0]==50): # D3
#        pin = 16
#    elif(args[0]==51): # D#3
#        pin = 5
