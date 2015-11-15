#!/usr/bin/env python
#SRIC script to be ran on the aircraft
import socket
import sys
import json
import NetworkManager
import uuid
import ftplib
import os
from pythonwifi.iwlibs import Wireless
#sockets
def sendfile (filename,sock):
	#connect and send to groundstation
	testdata = open(filename,'rb') #open a file
	line = testdata.read(1024)
	while(line):
	    print"Sending..."
	    sock.send(line)
	    line=testdata.read(1024)
	testdata.close()
	print"DONE"
	sock.shutdown(socket.SHUT_WR)

def receivefile(filename,sock):
	#receive a file on client side
	testrec = open(filename , 'wb') #open/create new file
	rline = sock.recv(1024)
	while (rline):
	    print rline
	    testrec.write(rline)
	    rline = sock.recv(1024)
	testrec.close()
	print "Received"
 #wireless  
def confignet (ssid, passkey, nickname):
	#Set up format for the wifi file
	network_connection = {
	    '802-11-wireless': {'mode': 'infrastructure',
						    'security': '802-11-wireless-security',
						    'ssid': ssid},
	     '802-11-wireless-security': {'auth-alg': 'open', 
		                          'key-mgmt': 'wpa-psk', 
		                          'psk': passkey},
	     'connection': {'id': nickname,
		            'type': '802-11-wireless',
		            'uuid': str(uuid.uuid4())},
	     'ipv4': {'method': 'auto'},#subnetmask
	     'ipv6': {'method': 'auto'}
	}
		
	NetworkManager.Settings.AddConnection(network_connection)

#FTP

def file_get(addr,usr,pwd,pth,file_name): #Gets files and stores it
    ftp = ftplib.FTP(addr)
    ftp.login(usr, pwd) 
    ftp.cwd(pth)
    ftp.retrlines("RETR " + file_name, open(file_name, 'wb').write )
    #os.rename(curpath,destpath)
    ftp.quit()

def file_send (addr,usr,pwd,pth,file_name): #Send a file
    ftp = ftplib.FTP(addr)
    ftp.login(usr, pwd)
    ftp.cwd(pth)
    ftp.storlines('STOR ' + file_name, open(file_name, 'r'))
    ftp.quit()
def recjson(conn):
	rline = conn.recv(1024)
	jsondata = json.loads(rline)
	conn.close()
	return jsondata


def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	IPGS = '192.168.0.6'
	IPAC = '192.168.0.2'
	Port = 9999
	Port2 = 8002
	sockr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((IPAC,Port))
	sock.listen(1) #wait for connection
	conn,address = sock.accept()
	data = recjson(conn)
	sock.close()
	ssid = data["ssid"]
	passkey = data["passkey"]
	addr = data["ftpIP"]
	usr = data["ftpuname"]
	pwd = data["ftppass"]
	pth = data["ftpfilelocation"]
	file_name = data["ftpfilename"]
	upfile_name = data["ftpupfilename"]
	confignet(ssid,passkey, "Nickname")
	wifi = Wireless('wlan1')
	statusssid = wifi.getEssid()
	while (statusssid != ssid):
		statusssid = wifi.getEssid()
	print ("Connected!")
	file_get(addr,usr, pwd, pth, file_name) #downloads a file to a specified path
	sockr.connect((IPGS,Port2))
	sendfile(file_name,sockr)
	receivefile(upfile_name,sockr)
	file_send(address,username,password,path,upfile_name)#uploads a file from a specified path
	
	print ("SUCCESS")
	sockr.close()    
main()



