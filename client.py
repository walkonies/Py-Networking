import socket as soc
import sys

HEADER = 64
PORT = 5050
SERVER = '192.168.1.198'
ADDR = (SERVER, PORT)
BUFFER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'

client = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
client.connect(ADDR)

def send(client, msg):
	message = msg.encode(FORMAT)
	size = len(message)
	bsize = str(size).encode(FORMAT)
	padding = HEADER - len(bsize)
	bsize += b' ' * padding # paddingto make length of header

	client.send(bsize)
	client.send(message)

	resp = client.recv(BUFFER_SIZE)
	if resp:
		print(resp.decode(FORMAT))

def chat():
	msg = input('msg: ')
	if msg == 'quit':
		send(client, DISCONNECT)
		return False
	send(client, msg)
	return True


def main():
	if len(sys.argv) > 1:
		global PORT
		PORT = int(sys.argv[1])
		print(PORT)

	running = True
	while running:
		running = chat()
		

if __name__ == '__main__':
	main()


