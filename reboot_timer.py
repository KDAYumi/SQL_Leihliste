#!/usr/bin/env python3

import os
import time
from time import sleep
import os


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
                #print(sql_host)
                
            if i==2:
                global sql_user
                sql_user=myline
                sql_user=sql_user.removeprefix("user=")
                sql_user=sql_user.strip()
                #print(sql_user)
                
            if i==3:
                global sql_password
                sql_password=myline
                sql_password=sql_password.removeprefix("password=")
                sql_password=sql_password.strip()
                #print(sql_password)
            if i==4:
                global sql_database
                sql_database=myline
                sql_database=sql_database.removeprefix("database=")
                sql_database=sql_database.strip()
                #print(sql_database)
            if i==6:
                global sql_bg_id
                sql_bg_id=myline
                sql_bg_id=sql_bg_id.removeprefix("bg_id=")
                sql_bg_id=sql_bg_id.strip()
                #print(sql_bg_id)
            if i==7:
                global sql_bg_name
                sql_bg_name=myline
                sql_bg_name=sql_bg_name.removeprefix("	bg_name=")
                sql_bg_name=sql_bg_name.strip()
                #print(sql_bg_name)
            if i==8:
                global sql_identifier
                sql_identifier=myline
                sql_identifier=sql_identifier.removeprefix("	identifier=")
                sql_identifier=sql_identifier.strip()
                #print(sql_identifier)
            if i==9:
                global sql_tag_uid
                sql_tag_uid=myline
                sql_tag_uid=sql_tag_uid.removeprefix("	tag_uid=")
                sql_tag_uid=sql_tag_uid.strip()
                #print(sql_tag_uid)
            if i==10:
                global sql_borrowed
                sql_borrowed=myline
                sql_borrowed=sql_borrowed.removeprefix("	borrowed=")
                sql_borrowed=sql_borrowed.strip()
                #print(sql_borrowed)
            if i==11:
                global sql_link
                sql_link=myline
                sql_link=sql_link.removeprefix("link=")
                sql_link=sql_link.strip()
                #print(sql_link)
            if i==12:
                global sql_bg__id
                sql_bg__id=myline
                sql_bg__id=sql_bg__id.removeprefix("	bg__id=")
                sql_bg__id=sql_bg__id.strip()
                #print(sql_bg__id)
            if i==13:
                global sql_name__id
                sql_name__id=myline
                sql_name__id=sql_name__id.removeprefix("	name__id=")
                sql_name__id=sql_name__id.strip()
                #print(sql_name__id)
            if i==14:
                global sql_date
                sql_date=myline
                sql_date=sql_date.removeprefix("	date=")
                sql_date=sql_date.strip()
                #print(sql_date)
            if i==15:
                global sql_name_id
                sql_name_id=myline
                sql_name_id=sql_name_id.removeprefix("name_id=")
                sql_name_id=sql_name_id.strip() 
                #print(sql_name_id)
            if i==16:
                global sql_first_name
                sql_first_name=myline
                sql_first_name=sql_first_name.removeprefix("	first_name=")
                sql_first_name=sql_first_name.strip() 
                #print(sql_first_name)
            if i==17:
                global sql_last_name
                sql_last_name=myline
                sql_last_name=sql_last_name.removeprefix("	last_name=")
                sql_last_name=sql_last_name.strip() 
                #print(sql_last_name)
            if i==18:
                global sql_user_uid
                sql_user_uid=myline
                sql_user_uid=sql_user_uid.removeprefix("	user_uid=")
                sql_user_uid=sql_user_uid.strip() 
                #print(sql_user_uid)
            if i==20:
                global path
                path=myline
                path=path.removeprefix("path=")
                path=path.strip() 
                #print(path)
            if i>20:
                break
            i=i+1
        myfile.close()

get_var()
while True:
    sleep(30)
    t = time.localtime()
    zeit= str(t.tm_hour)+str(t.tm_min)
    datum= str(t.tm_year)+"_"+str(t.tm_mday)+"-"+str(t.tm_mon)
    val=int(zeit)
    #print("mysqldump -u %s --password='%s' --databases='%s' > %s/backup/backup_%s.sql" %(sql_user,sql_password,sql_database,path,datum))
    if (val==0):
        passw="duagon"
        cmd="mysqldump -u %s --password='%s' --databases %s > %s/backup/backup_%s.sql" %(sql_user,sql_password,sql_database,path,str(datum))
        p=os.system('echo %s | sudo -S %s'%(passw,cmd))
        os.popen("sudo -S %s"%(cmd),'w').write(passw)
        print("%s/backup/backup_%s.sql wurde erfolgreich angelegt" %(path,datum))
        sleep(10)
        os.system("reboot")