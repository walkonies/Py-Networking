TIMEOUT = 10

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

def getUserName():
	pass