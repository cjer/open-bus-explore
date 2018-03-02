# -*- coding: utf-8 -*-

""" this program takes as input the number of a bus station,
	access the mabat.mot.gov.il web site, and retrieves the 
	bus line number and arrival time for each bus reaching the station"""

""" code and advice used in this program:

מידע על תחנה:
אם תשלח בקשת POST לכתובת הזאת:http://mabat.mot.gov.il/AdalyaService.svc/StationLinesByIdGet
ותשים בbody של הבקשה JSON כזה (תחליף את המספר במספר התחנה שבו אתה מעוניין)

{
    "stationId": 21451
}

או אם אתה בקטע של command line אתה מוזמן לשלוח את הפקודה הבאה:
curl -sd '{"stationId": 21451}' http://mabat.mot.gov.il/AdalyaService.svc/StationLinesByIdGet -H 'Content-Type: application/json' | python -m json.tool

==========

https://docs.python.org/2/library/commands.html

https://docs.python.org/2/library/subprocess.html

==========
command = "curl -sd '{\"stationId\": 21451}' http://mabat.mot.gov.il/AdalyaService.svc/StationLinesByIdGet -H 'Content-Type: application/json'"

jzon = os.popen(command)

string = jzon.read()

jzon = json.loads(string)

jzon['Payload']['Lines']

"""
#%%
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json 
import time
import sqlite3

conn = sqlite3.connect('linesInfo.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS linestats1
    (id INTEGER PRIMARY KEY, station_number INTEGER, time REAL, date TEXT, stationLines TEXT)''')    

"""
This code will receive a station ID number (an integer)), create the command
to access the mabat.mot.gov.il web site and retrieve the information as a json.
It returns a tuple of the station/bus lines information, epoch time and date/time """

def getInfo(station_number):
    """ given the station number, gets the json containing 
        bus arrival times and station info """    
    json_string = '{ "stationId": ' + str(station_number) + ', "isSIRI":true, "lang":"1037"}'
    command = "curl -sd '" + json_string + "' http://mabat.mot.gov.il/AdalyaService.svc/StationLinesByIdGet -H 'Content-Type: application/json'"
    timeAsked = time.time()
    timeHuman = time.ctime(timeAsked)
    handle = os.popen(command)
    responseText = handle.read()
    responseJson = json.loads(responseText)
    return (station_number, timeAsked, timeHuman, responseJson)

#%%
def saveInfo(responseTuple):
    """takes the tuple from getInfo(station_number) and stores in an sqlite database
        """
#create or connect to linesInfo database and table linestats 
    
    cur.execute('INSERT OR IGNORE INTO linestats1 (station_number, time, date, stationLines) VALUES (?, ?, ?, ?)', 
        (responseTuple[0], responseTuple[1],  responseTuple[2], str(responseTuple[3])) #['Payload']))
        )
    conn.commit()
#    cur.execute('SELECT * FROM linestats')    
#    cur.fetchone()
    


# THESE LINEs GETS 5 DATA POINTS FROM A SINGLE STATION, AND SAVES THEM IN THE DATABASE
for index in range(60):
    data1 = getInfo(25619)
    saveInfo(data1)
    time.sleep(60)    
    
#%%