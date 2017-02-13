#!/usr/bin/python

import sys
import RPi.GPIO as GPIO
import time
import json
import mysql.connector
from mysql.connector import Error

readings = {}

# Gather the configuration from the config.json
with open('config.json') as data_file:
    data = json.load(data_file)

    # Database credentials
    host = data["config"]["mysql"]["host"]
    user = data["config"]["mysql"]["user"]
    password = data["config"]["mysql"]["password"]
    db = data["config"]["mysql"]["db"]

    # Plants
    readings = []
    for plant in data["config"]["plants"]:
        readings.append({'channel': plant['gpio-channel'],'name': plant['plant-name'], 'reading': 'startingvalue'})


def write_to_database(reading_type, message):
    try:
        conn = mysql.connector.connect(host=host,
                                       database=db,
                                       user=user,
                                       password=password)
        if conn.is_connected():
            query = "INSERT INTO readings(type, message, datetime) " \
                    "VALUES(%s,%s)"
            args = (reading_type, message, time.strftime('%Y-%m-%d %H:%M:%S'))
            cursor = conn.cursor()
            cursor.execute(query, args)

    except Error as e:
        print(e)

    finally:
        conn.close()



# Loop over the readings and find the name
def find_channel_name (channel):
    for plant in readings:
        if plant['channel'] == channel:
            return plant['name']
    raise Exception('No plant with id ' + channel + ' could be found')


# This is the function we call when the state of the moisture changes
def callback(channel):
    name = find_channel_name(channel)

    if GPIO.input(channel) == readings[channel]:
        return
 
    if GPIO.input(channel):
        message = "Moisture no longer detected on plant " + name + " - Current date & time " + time.strftime("%c")
        write_to_database(0, message)
    else:
        message = "Moisture has been detected on plant " + name + " - Current date & time " + time.strftime("%c")
        write_to_database(1, message)

    print(message)
    readings[channel] = GPIO.input(channel)

# Set the mode
GPIO.setmode(GPIO.BCM)

# Register the gpio listening events
for plant in readings:
    GPIO.setup(plant['channel'], GPIO.IN)
    GPIO.add_event_detect(plant['channel'], GPIO.BOTH, bouncetime=300)
    GPIO.add_event_callback(plant['channel'], callback)

while True:
    time.sleep(0.1)
