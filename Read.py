#!/usr/bin/env python
#read.py
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
def read():
    
    reader = SimpleMFRC522()
    while True:
    #read data
        try:
            id, text = reader.read()
            print(id)          
            print(text)
            
        except KeyboardInterrupt:
            GPIO.cleanup()
read()