#!/usr/bin/env python
#SRIC script to be ran on the ground station

import socket
import sys
import json
import os
import re

def main():
        IPAC = '192.168.0.2'
        IPGS = '192.168.0.6'
        PORT = 9999
        PORT2 = 8002
        BUFFER_SIZE = 1024
        filename1 = "received"
        filename2 = "gs.txt"
        answer = 0
        #set up socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #confirm data with user
        while (answer != "1"):
                jsonobj = makejsonobj() #gathers info into a jason object
                print "------------------------------------------------"
                checkobj(jsonobj)
                print "\nPlease Make Sure the above data is correct!"
                answer = raw_input("Press 1 to send, 2 to reenter data: ")

        sock.connect((IPAC,PORT)) #connects

        sendjson(jsonobj,sock) #send over json obj

        recfile(sock,filename1) #recieve the file from the aircraft
        sendfile(sock,filename2)#sends a file to the aircraft
        sock.close()

#recieve file via socket
def recfile (conn,filename):
        newf = open(filename, 'wb') #open/create a file
        line = conn.recv(1024)
        while (line):
            print line
            newf.write(line)
            line = conn.recv(1024)
        newf.close()
        print "Received"

#send file via socket
def sendfile(conn,filename):
        replyfile = open(filename, 'rb') #opens the file for reading
        rline = replyfile.read(1024)
        while(rline):
            print ("Sending...")
            conn.send(rline)
            rline = replyfile.read(1024)
        print "SENT"

#configures an json object
#gets config data from gsconfig.txt
def makejsonobj():
        infile = open('gsconfig.txt', 'r')
        ssid = infile.readline()
        ssid = ssid.strip()
        
        passkey = infile.readline()
        passkey = passkey.strip()
        
        ftpip = infile.readline()
        ftpip = ftpip.strip()
        
        ftpuname = infile.readline()
        ftpuname = ftpuname.strip()
        
        ftppass = infile.readline()
        ftppass = ftppass.strip()
        
        ftpfilelocation = infile.readline()
        ftpfilelocation = ftpfilelocation.strip()
        
        ftpfilename = infile.readline()
        ftpfilename = ftpfilename.strip()
        
        ftpupfilename = infile.readline()
        ftpupfilename = ftpupfilename.strip()
        
        infile.close()

        network_json = {u'ssid': ssid, u'passkey': passkey,  u'ftpIP': ftpip, u'ftpuname': ftpuname, 				u'ftppass':ftppass,u'ftpfilelocation': ftpfilelocation, u'ftpfilename': ftpfilename, 				u'ftpupfilename':     ftpupfilename}
        return network_json

#configure data for checking
def checkobj(data):
        print ("ssid: ") +(data["ssid"])
        print ("passkey: ") + (data["passkey"])
        print ("address: ") + (data["ftpIP"])
        print ("username: ") + (data["ftpuname"])
        print ("password: ")+ (data["ftppass"])
        print ("path: ") + (data["ftpfilelocation"])
        print ("filename: ") + (data["ftpfilename"])
        print ("Our File Name: ") + (data["ftpupfilename"])

#sends a json object via sockets
def sendjson(jsonobj,sock):
        sline = json.dumps(jsonobj).encode('utf8')
        sock.send(sline)
        print "SENT"

main()
