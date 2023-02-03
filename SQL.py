#!/usr/bin/env python3

#SQL Datenbank: host='localhost', user='root', password='duagon', database='user_ids'

from __future__ import print_function
import inquirer
from time import sleep
import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import os
import subprocess

def get_var():
    i=1
    with open ('/home/duagon/bbt/setup.txt', 'rt') as myfile:  # Open lorem.txt for reading
        for myline in myfile:                                  # For each line, read to a string,
            #print(myline)                                      # and print the string.
            
            if i==1:
                global sql_host
                sql_host=myline
                sql_host=sql_host.removeprefix("host=")
                sql_host=sql_host.strip()
                print(sql_host)
                
            if i==2:
                global sql_user
                sql_user=myline
                sql_user=sql_user.removeprefix("user=")
                sql_user=sql_user.strip()
                print(sql_user)
                
            if i==3:
                global sql_password
                sql_password=myline
                sql_password=sql_password.removeprefix("password=")
                sql_password=sql_password.strip()
                print(sql_password)
            if i==4:
                global sql_database
                sql_database=myline
                sql_database=sql_database.removeprefix("database=")
                sql_database=sql_database.strip()
                print(sql_database)
            if i==6:
                global sql_bg_id
                sql_bg_id=myline
                sql_bg_id=sql_bg_id.removeprefix("bg_id=")
                sql_bg_id=sql_bg_id.strip()
                print(sql_bg_id)
            if i==7:
                global sql_bg_name
                sql_bg_name=myline
                sql_bg_name=sql_bg_name.removeprefix("	bg_name=")
                sql_bg_name=sql_bg_name.strip()
                print(sql_bg_name)
            if i==8:
                global sql_identifier
                sql_identifier=myline
                sql_identifier=sql_identifier.removeprefix("	identifier=")
                sql_identifier=sql_identifier.strip()
                print(sql_identifier)
            if i==9:
                global sql_tag_uid
                sql_tag_uid=myline
                sql_tag_uid=sql_tag_uid.removeprefix("	tag_uid=")
                sql_tag_uid=sql_tag_uid.strip()
                print(sql_tag_uid)
            if i==10:
                global sql_borrowed
                sql_borrowed=myline
                sql_borrowed=sql_borrowed.removeprefix("	borrowed=")
                sql_borrowed=sql_borrowed.strip()
                print(sql_borrowed)
            if i==11:
                global sql_link
                sql_link=myline
                sql_link=sql_link.removeprefix("link=")
                sql_link=sql_link.strip()
                print(sql_link)
            if i==12:
                global sql_bg__id
                sql_bg__id=myline
                sql_bg__id=sql_bg__id.removeprefix("	bg__id=")
                sql_bg__id=sql_bg__id.strip()
                print(sql_bg__id)
            if i==13:
                global sql_name__id
                sql_name__id=myline
                sql_name__id=sql_name__id.removeprefix("	name__id=")
                sql_name__id=sql_name__id.strip()
                print(sql_name__id)
            if i==14:
                global sql_date
                sql_date=myline
                sql_date=sql_date.removeprefix("	date=")
                sql_date=sql_date.strip()
                print(sql_date)
            if i==15:
                global sql_name_id
                sql_name_id=myline
                sql_name_id=sql_name_id.removeprefix("name_id=")
                sql_name_id=sql_name_id.strip() 
                print(sql_name_id)
            if i==16:
                global sql_first_name
                sql_first_name=myline
                sql_first_name=sql_first_name.removeprefix("	first_name=")
                sql_first_name=sql_first_name.strip() 
                print(sql_first_name)
            if i==17:
                global sql_last_name
                sql_last_name=myline
                sql_last_name=sql_last_name.removeprefix("	last_name=")
                sql_last_name=sql_last_name.strip() 
                print(sql_last_name)
            if i==18:
                global sql_user_uid
                sql_user_uid=myline
                sql_user_uid=sql_user_uid.removeprefix("	user_uid=")
                sql_user_uid=sql_user_uid.strip() 
                print(sql_user_uid)
            if i==20:
                global path
                path=myline
                path=path.removeprefix("path=")
                path=path.strip() 
                print(path)
            if i>20:
                break
            i=i+1
        myfile.close()

get_var()
sub= "%s/reboot_timer.py" % (path)
subprocess.Popen(sub,shell=False)

#disable error messages
GPIO.setwarnings(False)

# False here will cause the reader to stop reading
continue_reading = True

# declare the reader
reader = SimpleMFRC522()


#MySQL variables
mydb = mysql.connector.connect(host=sql_host, user=sql_user, password=sql_password, database=sql_database)
mycursor = mydb.cursor()
   
   
   



#Hauptmenü
def select_action():
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        questions = [
          inquirer.List('action',
                        message="Was hast du vor? ",
                        choices=['Baugruppe/tool ausleihen', 'neuen Datensatz anlegen', 'Datensatz auslesen','Ausgeliehene Baugruppen','Datensatz löschen'],
                        carousel = True,
                    ),
        ]
        answers = inquirer.prompt(questions)
        print(answers)
        if (answers == {'action':'Baugruppe/tool ausleihen'}):
            read_multi()
        if (answers == {'action':'neuen Datensatz anlegen'}):
            read_new_input_data()
        if (answers == {'action':'Datensatz auslesen'}):
            search()
        if (answers== {'action':'Ausgeliehene Baugruppen'}):
            search_link()
        if (answers== {'action':'Datensatz löschen'}):
            ask_scan()
           
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()


def ask_scan():

    try:
        question = [
          inquirer.List('action',
                        message="Tool oder User Löschen? ",
                        choices=['Tag scannen', 'User/Tool suchen'],
                    ),
        ]
        answers = inquirer.prompt(question)
        print(answers)
        if (answers == {'action':'Tag scannen'}):
            delete_scan()
        if (answers == {'action':'User/Tool suchen'}):
            delete_sel()
           
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
    
    
def delete_scan():

    try:
        # enable reader
        print("Bitte ein Tag scannen")      
        id, text = reader.read()
        print("ID: %s\n" % (id))
        uid=id
        
        # Tag ist ein User
        if is_registered('user',uid):
            # SQL Command
            sql = "SELECT * FROM %s WHERE %s = %s" %(sql_name_id,sql_user_uid,uid)
            mycursor.execute(sql)
    
            # SQL Output
            myresult = mycursor.fetchall()
            for x in myresult:
                trans_str=(x[0] + " " + x[1] +" "+ x[2])
        
            try:
                transfer = dict({'User': trans_str})
                print("i think this is a user")
                if input(trans_str + " löschen? (y/n)")=="y": 
                    remove_user(transfer)
                else:
                    select_action() 
            except:
                print("User not found")
                sleep(3)
                select_action()
            
        #remove user(uid,tag_status)

            
        # Tag ist ein Tool
        elif is_registered('tool',uid):
            trans_str = ("x "+"x "+str(uid))
            print("i think this is a tool")
            transfer = dict({'Tool': trans_str})
            if input(trans_str + " löschen? (y/n)")=="y":
              remove_tool(transfer)
            else:
              select_action()
            sleep(3)
        
        # Confirm to continue
        input("Drücke eine Taste um Fortzufahren")
        select_action()
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()


#search_link() sucht alle verknüpfungen von Usern und Tools
def search_link():

    try:  
        if (input("Möchten sie alle ausgeliehenen Baugruppen auslesen? (y/n) ") == "y"):
            # Login to the SQL Database
            
            # SQL Command
            sql = "SELECT * FROM %s" %(sql_link) 
            mycursor.execute(sql)

            #SQL Output
            myresult = mycursor.fetchall()
            for x in myresult:
                search_tool_link(x[0])
                search_user_link(x[1])
                print(x[2])
                print("")
            input("Drücke eine Taste um Fortzufahren")
            select_action() 
        else:
            select_action() 
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
  
  
# SQL request to add a new user
def insert_new_user(first,last,uid):

    try:
        # SQL Command
        sql = ("INSERT INTO %s (%s,%s,%s) VALUES ('%s','%s','%s')") %(sql_name_id,sql_first_name,sql_last_name,sql_user_uid,first, last, uid)
        print(sql)
        sleep(5)
        # Insert new user
        mycursor.execute(sql)
    
        # Make sure data is committed to the database
        mydb.commit()

    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
        
        
# SQL request to add a new user    
def insert_new_tool(bg_name, sn, uid):
    
    try:
        # SQL Command
        sql = ("INSERT INTO %s (%s, %s, %s) VALUES ('%s', '%s', %s)") %(sql_bg_id,sql_bg_name,sql_identifier,sql_tag_uid,bg_name, sn,  uid)
        print(sql)
        sleep(5)
    
        # Insert new tool
        mycursor.execute(sql)

        # Make sure data is committed to the database
        mydb.commit()
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
  
  
# Inputs für einen neuen User  
def give_name_inputs(uid):

    try:
        # Confirm variable
        yn= "n"
    
        # inputs for user data
        first_name = input("Vorname: ")
        last_name = input("Nachname: ")
    
        # Print to confirm
        print(first_name)
        print(last_name)
        print(uid)
        yn = input("Sind die Daten Korrekt? (y/n)")
        if yn == "y":
            insert_new_user(first_name,last_name, uid)
            print("Neuer Benutzer erfolgreich angelegt")
            sleep(3)
            select_action()
        else:
            give_name_inputs(uid)
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
        
        
# Inputs für eine neues Tool  
def give_tool_inputs(uid):
    
    try:
        
        # Confirm variable
        yn= "n"
        # inputs for tool data
        questions = [
        inquirer.Text("Tool", message="Definition: "),
        inquirer.Text("SN/Tool-Nummer", message="SN/Tool-Nummer: "),
        ]

        answers = inquirer.prompt(questions)
        print (answers)
    
        def_tool = answers['Tool']
        sn = answers['SN/Tool-Nummer']
        # Print to confirm
        print(def_tool)
        print(sn)
        print(uid)
        yn = input("Sind die Daten Korrekt? (y/n)")
    
        #Input to confirm
        if yn == "y":
            insert_new_tool(def_tool, sn, uid)
            print("Neue Baugruppe / Werkzeug erfolgreich angelegt")
            sleep(3)
            select_action()
        #Input abgebrochen
        else:
            give_tool_inputs(uid)
                        
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
  
  
   
# bg_id suche   
def search_tool(uid):
    
    try:
        # SQL Command
        sql = "SELECT * FROM %s WHERE %s LIKE %s" % (sql_bg_id,sql_tag_uid,uid)
        mycursor.execute(sql)

        # SQL Output
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()


# user_id suche
def search_user(uid):
    
    try:
        # SQL Command
        sql = "SELECT * FROM %s WHERE %s LIKE %s" % (sql_name_id,sql_user_uid,uid)
        mycursor.execute(sql)

        # SQL Output
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
 
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
 
 
def search_tool_link(uid):

    try:
        # SQL Command
        sql = "SELECT %s FROM %s WHERE %s LIKE %s" % (sql_bg_name,sql_bg_id,sql_tag_uid,uid)
        mycursor.execute(sql)
    
        # SQL Output
        myresult = mycursor.fetchall()
        print(myresult)
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()


#SQL Querry for User
def search_user_link(uid):
    
    try:
        # SQL Command
        sql = "SELECT %s, %s FROM %s WHERE %s LIKE %s" % (sql_first_name,sql_last_name,sql_name_id,sql_user_uid,uid)
        mycursor.execute(sql)
    
        # SQL Output
        myresult = mycursor.fetchall()
        print(myresult)
    
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
    
    
# search for a User/Tool 
def search():
    
    try:
        # enable reader
        print("Bitte ein Tag scannen")      
        id, text = reader.read()
        print("ID: %s\n" % (id))
        uid=id
        print(text)
        # Tag ist ein User
        if is_registered('user',uid):
            print(text)
            search_user_link(uid)
            uid = 0
            
        # Tag ist ein Tool
        else:
            if is_registered('tool',uid):
                print(text)
                search_tool_link(uid)
                uid = 0
            else:
                print("tag existiert nicht!")
                sleep(3)
                select_action()
        sleep(3)
        
        # Confirm to continue
        input("Drücke eine Taste um Fortzufahren")
        select_action()
   
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
        
   
# Tag prüfung User/Tool   
def read_new_input_data():
    
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        questions = [
          inquirer.List('action',
                        message="Tool oder User Anlegen? ",
                        choices=['Tool', 'User'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        print(answers)
        if (answers == {'action':'Tool'}):
            print("Bitte ein Tag scannen")
            reader.write("tag")
            id, text = reader.read()
            print("ID: %s\n" % (id))
            uid=id
            if is_registered("tool",uid) or is_registered("user",uid):
                print("Tag ist bereits registriert.")
                sleep(2)
                select_action()
            else:
                give_tool_inputs(uid)
                uid = 0
        if (answers == {'action':'User'}):
            # Insert a new User
            print("Bitte ein Tag scannen")
            id, text = reader.read()
            print("ID: %s\n" % (id))
            uid=id
            if is_registered("user",uid) or is_registered("tool",uid):
                print("Tag ist bereits registriert.")
                sleep(2)
                select_action()
            else:
                give_name_inputs(uid)
                uid = 0
                
        print("Erfolreich angelegt")
        sleep(3)
         
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
        
        
# NFC READ für Ausleihen
def read_multi():
    
    # enable reader
    try:
        
        #read Tags
        print("Bitte ein Tag scannen")      
        id, text = reader.read()
        print("ID: %s\n" % (id))
        uid=id
            
        # Prüfung, ob eine User Karte gescannt wurde
        if "tag" not in text:
            print("Bitte Kein User tag scannen")
            read_multi()
            
        #Search for Tool data 
        else:
            search_tool(uid)
            edit_tool_status(uid)
                
        sleep(3)
        select_action()
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
    
    
# User-Tool Verknüpfung in der link Datenbank
def link_user(tag_id,uid2):
    
    try:
        #SQL Command
        sql = "INSERT INTO %s (%s, %s) VALUES (%s, %s)" % (sql_link,sql_bg__id,sql_name__id,tag_id,uid2)
        mycursor.execute(sql)
        mydb.commit()

    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()


# Tool zurückgeben/ausleihen
def edit_tool_status(uid):
    
    try:
        # SQL Command 
        sql = "SELECT %s FROM %s WHERE %s LIKE %s" % (sql_borrowed,sql_bg_id,sql_tag_uid,uid)
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
    
        # SQL Output
        print(myresult)
    
        #Abfrage, ob Tool bereits ausgeliehen ist
        if(myresult == (0,)):
            print("Das gescannte Tag ist nicht ausgeliehen")
        
            # Input to confirm
            okay = input("Möchten sie die Baugruppe ausleihen? (y/n): ")
            if (okay == 'y'):
                tag_id = uid
            
                #enable reading
                try:
                
                    GPIO.cleanup()
                    print("Bitte User Tag Scannen")      
                    id, text = reader.read()
                    print(id)
                    uid2=id
                    
                    # Prüfung, ob eine User Karte gescannt wurde
                    if "tag" not in text:
                        
                        #Verknüpfung von User und Baugruppe
                        link_user(tag_id,uid2)
                        
                        
                        # SQL Command
                        sql = "UPDATE %s SET %s = True WHERE %s = %s" % (sql_bg_id,sql_borrowed,sql_tag_uid,tag_id)
                        mycursor.execute(sql)
                        mydb.commit()
                        
                        # Print out User Tag information
                        search_user(uid2)
                        uid = 0
                        
                        # Confirm message
                        print("Erfolgreich ausgeliehen! Viel spaß!")
                        sleep(3)
                        select_action()
                        
                    #exception handler
                    else:
                        print("Bitte ein USER Tag scannen")
                        
                except KeyboardInterrupt:
                    GPIO.cleanup()
                    select_action()
                
                
            # Baugruppe Zurückgeben
        else:
            print("Das gescannte Tag ist bereits ausgeliehen")
        
            #Input to confirm
            return_bg = input("Möchten sie das Tag zurrückgeben? (y/n): ")
            if (return_bg == "y"):
            
                #SQL Command
                text1 = "DELETE FROM %s WHERE %s = %s" % (sql_link,sql_bg__id,uid)
                mycursor.execute(text1)
                mydb.commit()
            
                #SQL Command
                text2 = "UPDATE %s SET %s = False WHERE %s = %s" % (sql_bg_id,sql_borrowed,sql_tag_uid,uid)
                mycursor.execute(text2)
                mydb.commit()
            
                # Confirmation message
                print("Tag erfolgreich zurückgegeben :)")
                
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
                     

#menu to sleect tool or user to delete
def delete_sel():
    
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        questions = [
          inquirer.List('action',
                        message="Tool oder User Löschen? ",
                        choices=['Tool', 'User'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        print(answers)
        if (answers == {'action':'Tool'}):
            del_tool()
        if (answers == {'action':'User'}):
            del_user()
           
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()


#menu to delete a tool
def del_tool():
    
    try:
        
        search = input("Suchbegriff: ")
        cb = search
        result=[]

        # SQL Command
        sql = "SELECT * FROM %s WHERE %s LIKE %s OR %s LIKE %s" % (sql_bg_id,sql_bg_name,("'"+"%"+ cb + "%" + "'"),sql_identifier,("'"+"%"+ cb + "%" + "'"))
        mycursor.execute(sql)
    
        # SQL Output
        myresult = mycursor.fetchall()
        for x in myresult:
            result.append(x[0] + " " + x[1] + " " + x[2])
       
    
        if not myresult:
            print("Kein Tool mit " +(cb)+ " gefunden!")
            sleep(3)
            select_action()
        else:    
            os.system('cls' if os.name == 'nt' else 'clear')
       
            try:
                questions = [
                  inquirer.List('Tool',
                                message="Welches Tool wollen sie Löschen? ",
                                choices=result,
                            ),
                ]
                answers = inquirer.prompt(questions)
                
            except KeyboardInterrupt:
                GPIO.cleanup()
                select_action()
                
        if input("Möchten sie %s Löschen? (y/n) " %(answers))=="y":
            print(answers)
            clear_tag()
            remove_tool(answers)
        else:
            select_action()
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
                
   
#SQL query to delete a tool
def remove_tool(tool):
    
    try:
        #Taking the Value out of the Dictionary
        ident = tool.get("Tool")
        split = ident.split()
        name = split[0]
        toolnr= split [1]
        uid = split[2]
        print(uid)
        print(name , split, ident, toolnr)
        if is_linked(uid)==False:
       
            # SQL Command
            sql = "DELETE FROM %s WHERE %s = %s " %(sql_bg_id,sql_tag_uid,uid)
            mycursor.execute(sql)
            mydb.commit()
            print(name+" "+ident+" erfolgreich gelöscht") 
            sleep(2)
            select_action()
        else:
            print("is borrowed")
            print(uid)
            if (input("Verknüpfung entfernen und löschen? (y/n) ")=="y"):
           

                # SQL Command
                sql = "DELETE FROM %s WHERE %s = %s " %(sql_bg_id,sql_tag_uid,uid)
                mycursor.execute(sql)
                mydb.commit()
                sleep(1)
                sql = "DELETE FROM %s WHERE %s = %s " %(sql_link,sql_bg__id,uid)
                mycursor.execute(sql)
                mydb.commit()
                print(name+" "+ident+" erfolgreich entlinkt und gelöscht") 
                sleep(1)
                input("Drücke eine Taste um Fortzufahren")
                select_action()
                
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
       
       
#menu to delete a user    
def del_user():
    
    try:
        search = input("Suchbegriff: ")
        result=[]

        # SQL Command
        sql = "SELECT * FROM %s WHERE %s or %s LIKE %s" %(sql_name_id,sql_first_name,sql_last_name,("'"+"%"+ search + "%" + "'"))
        mycursor.execute(sql)
    
        # SQL Output
        myresult = mycursor.fetchall()
        for x in myresult:
            result.append(x[0] + " " + x[1] +" "+ x[2])
        
        print(myresult)
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            questions = [
              inquirer.List('User',
                            message="Welchen User wollen sie Löschen? ",
                            choices=result,
                        ),
            ]
            answers = inquirer.prompt(questions)
        except KeyboardInterrupt:
            GPIO.cleanup()
            select_action()
        if input("Möchten sie %s Löschen? (y/n) " %(answers))=="y":
            remove_user(answers)
        else:
            select_action()

    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
        
        
#SQL query to delete the user 
def remove_user(user):
    
    try:
        ident=user.get("User")
        split=ident.split()
        first=split[0]
        last=split[1]
        uid=split[2]
    
        if is_linked(uid)==False:
        
            # SQL Command
            sql = "DELETE FROM %s WHERE %s = %s" %(sql_name_id,sql_user_uid,uid)
            mycursor.execute(sql)
            mydb.commit()
            print(first+ " " + last + " erfolgreich gelöscht") 
            sleep(2)
            select_action()
        else:
            print(first+" "+last+" Hat noch ausgeliehene Baugruppen! BITTE ZUERST ALLES ZURÜCKBRINGEN!")
            sleep(2)
            search_user_linked(uid)
    
        select_action()
    
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
    
    
#replaces all data on the tag with "empty"    
def clear_tag():
    try:
        print("Bitte Tag erneut scannen")
        reader.write("empty")
        print("Tag cleared")
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
    finally:
        GPIO.cleanup()
        
     
     
#outputs all users with the given UID        
def search_user_linked(uid):
    
    try:
        # SQL Command 
        sql = "SELECT %s FROM %s WHERE %s = %s" % (sql_bg__id,sql_link,sql_name__id,uid)
        mycursor.execute(sql)
        myresult=mycursor.fetchall()
    
        for x in myresult:
            sql= "SELECT %s AND %s FROM %s WHERE %s = %s" % (sql_bg_name,sql_identifier,sql_bg_id,sql_tag_uid,x)
            mycursor.execute(sql)
            myresul=mycursor.fetchall()
            for y in myresul:
                print(y)
    
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
           
           
#checks for uid references in the link database            
def is_linked(uid):
    
    try:
        sql= "SELECT * FROM link WHERE (%s = %s OR %s = %s)" % (sql_name__id,uid,sql_bg__id,uid)
        mycursor.execute(sql)
        myresult=mycursor.fetchall()
        for x in myresult:
            print(x)
        if myresult:
            return True
        else:
            return False
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
        return None
 
 
#checks for already existing UID 
def is_registered(u_t,uid):
    
    try:
        if (u_t=="tool"):
            sql= "SELECT * FROM %s WHERE %s = %s" % (sql_bg_id,sql_tag_uid,uid)
            mycursor.execute(sql)
            myresult=mycursor.fetchone()
            if myresult:
                return True
            else:
                return False
        elif(u_t=="user"):
            sql= "SELECT * FROM %s WHERE %s = %s" % (sql_name_id,uid,sql_user_uid)
            mycursor.execute(sql)
            myresult=mycursor.fetchone()
            if myresult:
                return True
            else:
                return False
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        select_action()
        return None
 
 
#MAIN
if __name__ == "__main__":
    
    select_action()