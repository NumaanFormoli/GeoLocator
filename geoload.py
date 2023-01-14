# simulating or using the google places api to find locations from these locations
# visualize them onto a map


# geoload.py reads where.data
# geoload.opy should be able to blow and simply restart

import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

# need api key
api_key = "AIzaSyDbkfVbTcGPEJRI4ESpYmbLQffBGG9pAQ0"
serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# additional detail for urllib
# http.client.HTTPConneciton.debuglevel = 1

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore the SSL Certificate errors; Python doesn't ship with any legitmate certificates
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("where.data")
count = 0

for line in fh:
    if count > 200:
        print('Retrieved 200 locations, restart to retrieve more')
        break

    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address= ?", (memoryview(address.encode()), ))
    
    # check if the address is already located in the database
    try:
        #grabs it and finds it in database; useful when restarting
        data = cur.fetchone()[0]
        print("Found in database ", address) 
        continue
    except:
        pass
    # make dictionary for the parameters of the url query
    parms = dict()
    parms["address"] = address
    parms['key'] = api_key
    
    # urlencode adds all the +s and nice stuff
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context = ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

    try:
        js = json.loads(data)
    except:
        print(data)
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('Failure to Retrieve')
        print(data)
        break

    cur.execute('''INSERT INTO Locations (address, geodata) VALUES (?, ?)''', (memoryview(address.encode()), memoryview(data.encode())))
    conn.commit()
    if count % 10 == 0 :
        print('Pausing for a bit....')
        time.sleep(5)



# loop through it and pull out the address
# select from geodata where that address is the address, 
# check if in dataabse, if so continue otherwise keep going