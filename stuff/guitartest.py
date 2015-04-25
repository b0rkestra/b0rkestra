
#!/usr/bin/env python   
import sys
from time import sleep
import threading
import RPi.GPIO as GPIO
from RPIO import PWM


gpiopin = [3, 5, 7, 11, 13, 15]
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(gpiopin[0], GPIO.OUT)
GPIO.setup(gpiopin[1], GPIO.OUT)
GPIO.setup(gpiopin[2], GPIO.OUT)
GPIO.setup(gpiopin[3], GPIO.OUT)
GPIO.setup(gpiopin[4], GPIO.OUT)
GPIO.setup(gpiopin[5], GPIO.OUT)
gpio = GPIO

gpio.output(gpiopin[0],True)
gpio.output(gpiopin[1],True)
gpio.output(gpiopin[2],True)
gpio.output(gpiopin[3],True)
gpio.output(gpiopin[4],True)
gpio.output(gpiopin[5],True)



for i in range(3):
    gpio.output(gpiopin[0],False)
    sleep(0.1)
    gpio.output(gpiopin[0],True)
    sleep(0.5)

    gpio.output(gpiopin[1],False)
    sleep(0.1)
    gpio.output(gpiopin[1],True)
    sleep(0.5)

    gpio.output(gpiopin[2],False)
    sleep(0.1)
    gpio.output(gpiopin[2],True)
    sleep(0.5)

    gpio.output(gpiopin[3],False)
    sleep(0.1)
    gpio.output(gpiopin[3],True)
    sleep(0.5)

    gpio.output(gpiopin[4],False)
    sleep(0.1)
    gpio.output(gpiopin[4],True)
    sleep(0.5)

    gpio.output(gpiopin[5],False)
    sleep(0.1)
    gpio.output(gpiopin[5],True)
    sleep(0.5)
    print('hit')

GPIO.cleanup() 
PWM.cleanup()


print('fin')
