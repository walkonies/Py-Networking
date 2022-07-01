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

def handleClient(client):
	print(f'[NEW CONNECTION] {client.name}:{client.addr} connected.')
	connected = True
	while connected:
		mesg_length = client.conn.recv(HEADER).decode(FORMAT)
		if mesg_length:
			mesg_length = int(mesg_length)
			connected = handleMessage(client, mesg_length)
	disconnectClient(client)

def handleMessage(client, size):
	print(f'[INCOMING] {size}bytes')
	msg = client.conn.recv(size).decode(FORMAT)

	if msg == DISCONNECT:
		sendAck(client.conn, msg='DISCONNECTED')
		return False

	sendAck(client.conn)
	displayMsg(client, msg)
	return True

def newConnection(conn, addr):
	user = getUserName(addr)
	if not user:
		sendAck('[NEW USER] ENTER NAME')
		getNewUser(addr)
	else:
		sendAck(f'[WELCOME] {user}')

	client = Client(conn, addr, name)
	handleClient(client)

def disconnectClient(client):
	print(f'[DISCONNECT] {client.addr[0]}')
	client.conn.close()

	connections = threading.activeCount()-2 # one for main one for this thread
	print(f'[ACTIVE CONNECTIONS] {connections}')
	if connections < 1:
		systemSleep()

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
		sendAck(conn, msg=f'CONNECTED TO {NAME}')
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
	