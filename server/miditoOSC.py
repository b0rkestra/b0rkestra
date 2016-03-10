#!/usr/bin/env python
#
# test_midiin_callback.py
#
"""Shows how to receive MIDI input by setting a callback function."""

import logging
import sys
import time
import argparse
import random
import time


import OSC

import rtmidi
from rtmidi.midiutil import open_midiport

log = logging.getLogger('test_midiin_callback')

logging.basicConfig(level=logging.DEBUG)


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

        self.c = OSC.OSCClient()
        #self.c = OSC.OSCMultiClient()

        #self.c.connect()  
        #self.c.connect(('255.255.255.255', 7110))  


    def __call__(self, event, data=None):
        message, deltatime = event

        #self._wallclock += deltatime
        #print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        #message needs to be the midi message encapsualted in osc for network tx
        #print(event)
        

        message = event[0]
        # check controller number
        firstbit = message[0] >> 4
        chan = message[0] & 15

        #Control change
        if (firstbit == 11) and message[1] == 13:
            # map controller value
            #event[2] = int(self._map(event[2]))
            print(message)
            #oscsend('path',firstbit)

        #note on / off
        elif ((firstbit ==9) or (firstbit ==8)):
          #  path = '/drums/'+str(chan)+'/noteon/'  
            path = ""
            if (chan == 15):
                print "durms"
                path = "/drums/1"
            elif (chan == 0):
                print "siren"
                path = "/siren/1"
            elif (chan == 1):
                print "sunguitar"
                path = "/sunguitar/1"
            elif (chan == 3):
                print "tubulum"
                path = "/tubulum/1"
            elif (chan == 2):
                path = "/racketguitar/1"
                print "racket"
            else:
                print "no instrument on channel", chan
                return 
            value = [message[1],message[2]]
            if(firstbit ==8):
                value = [message[1],0]
            
            print(value)

            self.oscsend(path,value)



    def oscsend(self,path,val):    
        print('send')
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress(path)
        oscmsg.append(val)

#       def sendto(self, msg, address, timeout=None):


        #self.c.sendto(oscmsg,("192.168.1.13",7110))
        #self.c.sendto(oscmsg,("255.255.255.255",7110))
        self.c.sendto(oscmsg,("192.168.1.255",7110))


port = sys.argv[1] if len(sys.argv) > 1 else None
try:
    midiin, port_name = open_midiport(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    # just wait for keyboard interrupt in main thread
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    self.oscsend('/quit',2)
    midiin.close_port()
    del midiin



