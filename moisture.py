#!/usr/bin/python

# Start by importing the libraries we want to use

import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import time # This is the time library, we need this so we can use the sleep function

lastReading = 'STARTINGVALUE'

readings = {}
readings[14] = 'startingvalue'
readings[15] = 'startingvalue'

# This is our callback function, this function will be called every time there is a change on the specified GPIO channel, in this example we are using 17
def callback(channel):

	if channel == 14:
		name = 'Plant 4'
	else:
		name = 'Plant 5'

	if GPIO.input(channel) == readings[channel]:
		return
 
	if GPIO.input(channel):
		message = "Moisture no longer detected on plant " + name +  " - Current date & time " + time.strftime("%c")
		sendTextMessage('07903869591', message)
		print message
	
	readings[channel] = GPIO.input(channel)
		

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel = 14
GPIO.setup(channel, GPIO.IN)
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

#
channel = 15
GPIO.setup(channel, GPIO.IN)
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

# This is an infinte loop to keep our script running
while True:
	# This line simply tells our script to wait 0.1 of a second, this is so the script doesnt hog all of the CPU
	time.sleep(0.1)
