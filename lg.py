#!/usr/bin/env python3
#Full list of commands
#http://developer.lgappstv.com/TV_HELP/index.jsp?topic=%2Flge.tvsdk.references.book%2Fhtml%2FUDAP%2FUDAP%2FAnnex+A+Table+of+virtual+key+codes+on+remote+Controller.htm

print('Starting application')

import http.client
from tkinter import *
import xml.etree.ElementTree as etree
import socket
import re
import sys
import time
print('LG Smart TV remote command')

lgtv = {}
dialogMsg =""
headers = {"Content-Type": "application/atom+xml"}

#Important authorization key showed in Smart TV
lgtv["pairingKey"] = "099999"

print('Connecting LG Smart TV')

def getip():
    strngtoXmit =   'M-SEARCH * HTTP/1.1' + '\r\n' + \
                    'HOST: 239.255.255.250:1900'  + '\r\n' + \
                    'MAN: "ssdp:discover"'  + '\r\n' + \
                    'MX: 2'  + '\r\n' + \
                    'ST: urn:schemas-upnp-org:device:MediaRenderer:1'  + '\r\n' +  '\r\n'
    bytestoXmit = strngtoXmit.encode()
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.settimeout(3)
    found = False
    gotstr = 'notyet'
    i = 0
    ipaddress = None
    sock.sendto( bytestoXmit,  ('239.255.255.250', 1900 ) )
    while not found and i <= 5 and gotstr == 'notyet':
        try:
            gotbytes, addressport = sock.recvfrom(512)
            gotstr = gotbytes.decode()
        except:
            i += 1
            sock.sendto( bytestoXmit, ( '239.255.255.250', 1900 ) )
        if re.search('LG', gotstr):
            ipaddress, _ = addressport
            found = True
        else:
            gotstr = 'notyet'
        i += 1
    sock.close()
    if not found : sys.exit("Lg TV not found")
    return ipaddress

def displayKey():
    conn = http.client.HTTPConnection( lgtv["ipaddress"], port=8080)
    reqKey = "<!--?xml version=\"1.0\" encoding=\"utf-8\"?--><auth><type>AuthKeyReq</type></auth>"
    conn.request("POST", "/roap/api/auth", reqKey, headers=headers)
    httpResponse = conn.getresponse()
    if httpResponse.reason != "OK" : sys.exit("Network error")
    return httpResponse.reason

def getSessionid():
    conn = http.client.HTTPConnection( lgtv["ipaddress"], port=8080)
    pairCmd = "<!--?xml version=\"1.0\" encoding=\"utf-8\"?--><auth><type>AuthReq</type><value>" \
            + lgtv["pairingKey"] + "</value></auth>"
    conn.request("POST", "/roap/api/auth", pairCmd, headers=headers)
    httpResponse = conn.getresponse()
    if httpResponse.reason != "OK" : return httpResponse.reason
    tree = etree.XML(httpResponse.read())
    return tree.find('session').text

def getPairingKey():
    displayKey()

def handleCommand(cmdcode):
    conn = http.client.HTTPConnection( lgtv["ipaddress"], port=8080)
    cmdText = "<!--?xml version=\"1.0\" encoding=\"utf-8\"?--><command>" \
                + "<name>HandleKeyInput</name><value>" \
                + cmdcode \
                + "</value></command>"
    conn.request("POST", "/roap/api/command", cmdText, headers=headers)
    httpResponse = conn.getresponse()

#main()
lgtv["ipaddress"] = getip()
#lgtv["ipaddress"] = '192.168.1.33'

theSessionid = getSessionid()
while theSessionid == "Unauthorized" :
    getPairingKey()
    time.sleep(0.5)
    theSessionid = getSessionid()

if len(theSessionid) < 8 : sys.exit("Could not get Session Id: " + theSessionid)
lgtv["session"] = theSessionid
print(lgtv)

#displayKey()
#result = str(sys.argv[1])
#handleCommand(result)

print(sys.argv)
if len(sys.argv) < 2:
   print('Should be entered an argument with someone command:')
   print('1 - POWER')
   print('2 - Number 0')
   print('3 - Number 1')
   print('4 - Number 2')
   print('5 - Number 3')
   print('6 - Number 4')
   print('7 - Number 5')
   print('8 - Number 6')
   print('9 - Number 7')
   print('10 - Number 8')
   print('11 - Number 9')
   print('12 - UP key among remote Controller’s 4 direction keys')
   print('13 - DOWN key among remote Controller’s 4 direction keys')
   print('14 - LEFT key among remote Controller’s 4 direction keys')
   print('15 - RIGHT key among remote Controller’s 4 direction keys')
   print('20 - OK')
   print('21 - Home menu')
   print('22 - Menu key (same with Home menu key)')
   print('23 - Previous key (Back)')
   print('24 - Volume up')
   print('25 - Volume down')
   print('26 - Mute (toggle)')
   print('27 - Channel UP (+)')
   print('28 - Channel DOWN (-)')
   print('29 - Blue key of data broadcast')
   print('30 - Green key of data broadcast')
   print('31 - Red key of data broadcast')
   print('32 - Yellow key of data broadcast')
   print('33 - Play')
   print('34 - Pause')
   print('35 - Stop')
   print('36 - Fast forward (FF)')
   print('37 - Rewind (REW)')
   print('38 - Skip Forward')
   print('39 - Skip Backward')
   print('40 - Record')
   print('41 - Recording list')
   print('42 - Repeat')
   print('43 - Live TV')
   print('44 - EPG')
   print('45 - Current program information')
   print('46 - Aspect ratio')
   print('47 - External input')
   print('48 - PIP secondary video')
   print('49 - Show / Change subtitle')
   print('50 - Program list')
   print('51 - Tele Text')
   print('52 - Mark')
   print('400 - 3D Video')
   print('401 - 3D L/R')
   print('402 - Dash (-)')
   print('403 - Previous channel (Flash back)')
   print('404 - Favorite channel')
   print('405 - Quick menu')
   print('406 - Text Option')
   print('407 - Audio Description')
   print('408 - NetCast key (same with Home menu)')
   print('409 - Energy saving')
   print('410 - A/V mode')
   print('411 - SIMPLINK')
   print('412 - Exit')
   print('413 - Reservation programs list')
   print('414 - PIP channel UP')
   print('415 - PIP channel DOWN')
   print('416 - Switching between primary/secondary video')
   print('417 - My Apps')
   sys.exit(1)

for result in sys.argv:
   if result != sys.argv[0]:
      time.sleep(0.1)
      handleCommand(str(result))

