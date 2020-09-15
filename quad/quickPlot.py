import serial
import time 
usb = '/dev/tty.usbmodem1423'
telem =  '/dev/tty.usbserial-DN02136Z'
board = serial.Serial(port = usb, baudrate = 57600, timeout = 3)
time.sleep(3)

angleData = open('anglesData.txt', 'w')

print("Starintg")

while(1):
		try:
			data = board.readline()
			angleData.write(data)
			print(data)
			board.reset_input_buffer
		except KeyboardInterrupt:
			angleData.close()
			
