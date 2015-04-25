
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

GPIO.setmode(GPIO.BOARD)  
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)


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
    pin =3
    
    if(args[0]==60):
        pin = 3     
    elif(args[0]==61):
        pin = 5
    elif(args[0]==62):
        pin =7   
    elif(args[0]==63):
        pin = 11
    elif(args[0]==64):
        pin =13
    elif(args[0]==65):
        pin =15 

    
    vel = args[1]
    print('vel',vel)

    FuncThread(hit, GPIO, pin,vel).start()



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
