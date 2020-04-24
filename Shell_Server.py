import socket
import sys

def create_socket():
	try :
		global socks
		global host
		global port
		host = '0.0.0.0'
		port = 666
		socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print (f"Socket Created For IP = {host} on Port = {port} ")
	except :
		print ("Error In Creating Sockets. ")
		print ("Retrying")
		create_socket()

def socket_bind():
	try :
		global host
		global port
		global socks
		print (f"Binding to Port = {port} ")
		socks.bind((host,port))
		print ("Bind Successful")

	except :
		print ("Bind unsuccessful. Retrying...")
		socket_bind()

def accept_connection():
	global socks
	socks.listen(3)
	print("Listening for Connection....")
	conn , addr = socks.accept()
	print(f"Connection established with IP :{addr[0]} on Port : {addr[1]}")
	cac(conn)
	conn.close()

def cac(conn):
	while True:
		cmd = input(":>")
		
		if cmd[:2] == 'cd':
			conn.send(cmd.encode('utf-8'))
			print('\n')
			
		elif cmd[:5] == 'fetch' :
			conn.send(cmd.encode('utf-8'))
			freq = input("Enter the name of the file to download :")
			
			count = 0
			fname= input("Enter New name of the incoming file : ")
			conn.send(freq.encode("utf-8"))
			recvfile = open(fname,'wb')
			while count >= 0 :
				data = conn.recv(102400)
				count = count + 1 
				print(f"Receive Count :{count} ")
				if data :
					recvfile.write(data)
					
				else :
					print("Received \n")
					count = -1
	
			recvfile.close()
			conn.close()
			accept_connection()
				
		elif ((len(cmd) >0) and (cmd != " ") and (cmd != 'quit')) :
			conn.send(cmd.encode('utf-8'))
			response = conn.recv(102400).decode('utf-8') + " "
			print('\n' + response)
			
		elif cmd == 'quit':
			conn.send(cmd.encode('utf-8'))
			conn.close()
			socks.close()
			sys.exit(0)

def main():
	create_socket()
	socket_bind()
	accept_connection()

main()
