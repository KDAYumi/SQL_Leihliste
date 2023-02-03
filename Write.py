#!/usr/bin/env python
#write.py
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522



def write():
    reader = SimpleMFRC522()
    GPIO.setwarnings(False)
    
    #write data
    try:
            text = input('New data:')
            print("Now place your tag to write")
            reader.write(text)
            print("Written")
    finally:
            GPIO.cleanup()
        
write()