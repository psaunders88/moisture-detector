#!/usr/bin/python

# Start by importing the libraries we want to use

import json
from twilio.rest import TwilioRestClient
import time # This is the time library, we need this so we can use the sleep function

with open('config.json') as data_file:    
    data = json.load(data_file)
    sid = data.twilio.sid
    secret = data.twilio.secret
    client = TwilioRestClient(sid, secret)
    sendto = data.twilio.sendto
    from_ = data.twilio.from_


# Function for sending a text message using the twilio api
def sendTextMessage(whoTo, message):
    client.messages.create(to=whoTo, from_=from_, body=message)
