TIMEOUT = 10
USERS = 'users.csv'
FORMAT = 'utf-8'
HEADER = 64

class Client:
	def __init__(self, conn, addr, name):
		self.conn = conn
		self.addr = addr
		self.name = name

def sendAck(conn, msg=None):
	if not msg:
		msg = 'Message received!'
	msg = msg.encode(FORMAT)
	conn.send(msg)

def displayMsg(user, msg):
	print(f'[{user}] {msg}')

def systemSleep():
	sleeping = False
	connections = threading.activeCount()-2
	while connections < 1:
		if not sleeping:
			sleeping = True
			print(f'[SLEEPING] {TIMEOUT}s')
			sleep = time.time() + TIMEOUT
		else:
			timer = sleep-time.time()
			if timer < 0:
				shutdown()
				break
			elif int(timer) == TIMEOUT//2:
				print(f'[SLEEPING] {TIMEOUT//2}s')
		time.sleep(1)
		connections = threading.activeCount()-2
	
	else:
		print('[AWAKE]')
		sleeping = False

def readCSV(file):
	data = {}
	sep = ','
	with open(file, 'r') as f:
		file_data = f.read().split('\n')
		file_data.pop(-1) # remove newline at EOF
	
	for line in file_data:
		addr, name = line.split(sep)
		data[addr] = name
	return data

def updateCSV(file, data):
	sep = ','
	data = list(data)

	line = sep.join(data)
	with open(file, 'a') as f:
		f.write(line + '\n')	

def getUserName(addr):
	users = readCSV(USERS)
	name = None
	if addr in users.keys():
		name = users[addr]
	return name

def getNewUser(conn, addr):
	name = conn.recv(HEADER).decode(FORMAT).rstrip()
	updateCSV(USERS, (addr, name))
	return name

if __name__ == '__main__':
	pass