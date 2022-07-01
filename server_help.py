TIMEOUT = 10
USERS = 'users.csv'

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
				running = False
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

def getUserName(addr):
	users = readCSV(USERS)
	if addr in users.keys():
		return users[addr]
	else:
		return None

def setUserName(addr):
	pass



if __name__ == '__main__':
	pass