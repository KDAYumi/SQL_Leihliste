import mfrc522
# Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")
continue_reading=True
MIFAREReader=mfrc522()
# This loop keeps checking for chips. If one is near it will get the UID  and authenticate
while continue_reading:

# Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

# If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")

# Get the UID of the card
    status,uid = MIFAREReader.MFRC522_Anticoll()

# If we have the UID, continue
    if status == MIFAREReader.MI_OK:

    # Print UID
        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

    # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        setas = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x07,0x80,0x69,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        sect = 7
    # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

    # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, sect, key, uid)

    # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(sect)

            MIFAREReader.MFRC522_Write(sect,setas)

            MIFAREReader.MFRC522_Read(sect)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print ("Authentication error")