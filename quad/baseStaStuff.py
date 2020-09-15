def resetMenu(option):

	print("Please choose one of the following options to view:")
	print("1. Angle Data")
	print("2. PID Output")
	print("3. PID vs Angles")
	print("4. Gains")
	print("Press Ctrl + C to exit data streaming")
	option = raw_input("Choose your option: ")
	
	board.write('send')
	board.write(option)
	
	return option

def readData():
	while board.in_waiting < 1:
		pass
	data = board.readline()
	board.write('send')
	board.write(option)
	return data

	
