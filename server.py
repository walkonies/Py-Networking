import socket as soc
import threading
import time
import sys
import pandas as pd
from server_help import *

NAME = "ALEX'S SERVER"
HEADER = 64
PORT = 5050
BUFFER_SIZE = 1024
SERVER = soc.gethostbyname(soc.gethostname())  # local IP address
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
USERS = pd.read_csv('users.csv')

threads = []
running = False
server = None

def handleClient(conn, addr):
	user = getUserName(conn, addr)
	print(f'[NEW CONNECTION] {addr} connected.')
	#sendAck(conn, msg=f'CONNECTED TO {NAME}')
	
	connected = True
	while connected:
		mesg_length = conn.recv(HEADER).decode(FORMAT)
		if mesg_length:
			mesg_length = int(mesg_length)
			print(f'[INCOMING] {mesg_length}bytes')
			msg = conn.recv(mesg_length).decode(FORMAT)

			if msg == DISCONNECT:
				connected = False
				sendAck(conn, msg='DISCONNECTED')
				break

			sendAck(conn)
			displayMsg(addr, msg)

	disconnectClient(conn, addr)

def disconnectClient(conn, addr):
	print(f'[DISCONNECT] {addr[0]}')
	conn.close()

	connections = threading.activeCount()-2 # one for main one for this thread
	print(f'[ACTIVE CONNECTIONS] {connections}')
	
	if connections < 1:
		systemSleep()

def sendAck(conn, msg=None):
	if not msg:
		msg = 'Message received!'
	msg = msg.encode(FORMAT)
	conn.send(msg)

def displayMsg(addr, msg):
	print(f'[{addr[0]}] {msg}')

def shutdown():
	print(f'[SHUTTING DOWN] {NAME}')
	server.close()

def start(s):
	global running, server
	running = True
	server = s
	server.listen()
	sleeping = False

	while running:
		conn, addr = server.accept()
		thread = threading.Thread(target=handleClient, args=(conn,addr))
		thread.start()
		threads.append(thread)

		connections = threading.activeCount()-1
		print(f'[ACTIVE CONNECTIONS] {connections}')

def main():
	if len(sys.argv) > 1:
		global PORT
		PORT = int(sys.argv[1])
		print(PORT)

	ADDR = (SERVER, PORT)
	server = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
	server.bind(ADDR)

	print(f'[STARTING] {NAME} IS RUNNING...\tPORT:{PORT}')
	start(server)

if __name__ == '__main__':
	main()
	