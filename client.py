import socket as soc
import sys

HEADER = 64
PORT = 5050
SERVER = '192.168.1.198'
WORK = '104.51.152.244'
BUFFER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
CONNECT = '!CONNECT'

def send(client, msg):
	message = msg.encode(FORMAT)
	size = len(message)
	bsize = str(size).encode(FORMAT)
	padding = HEADER - len(bsize)
	bsize += b' ' * padding # paddingto make length of header

	client.send(bsize)
	client.send(message)


def chat(client):
	msg = input('msg: ')
	if msg == 'quit':
		send(client, DISCONNECT)
		return False
	send(client, msg)
	return True

def connectClient(addr):
	server, port = addr
	print(f'[CONNECTING] {server} PORT:{port}')
	client = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
	client.connect(addr)
	send(client, CONNECT)
	client.recv(HEADER)
	return client

def start(client):
	running = True
	while running:
		resp = client.recv(BUFFER_SIZE)
		if resp:
			print(resp.decode(FORMAT))

		running = chat(client)

def main():
	if len(sys.argv) > 1:
		global PORT
		PORT = int(sys.argv[1])
		print(PORT)

	ADDR = (WORK, PORT)

	client = connectClient(ADDR)
	start(client)
		
if __name__ == '__main__':
	main()


