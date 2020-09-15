import matplotlib.pyplot as chart
import numpy as np

def getAngles(data, angleData):
	data = readData()
	rMark = data.find('r')
	pMark = data.find('p')
	yMark = data.find('y')
	sMark = data.find('s')
	aMark = data.find('a')
		
	checksum = 0

	if sMark == 0:
		if aMark == 1:
			if (rMark - aMark) - 1 > 7:  
				rollAngle = data[aMark+1:rMark]
				checksum = 1

			if (pMark - rMark) - 1 > 7:
				pitchAngle = data[rMark+1:pMark]
				checksum = 2
			
			if (yMark - pMark) - 1 > 7:
				yawAngle = (data[pMark+1:yMark])
				checksum = 3
	
	if checksum == 3:
		angleData.write(rollAngle+','+pitchAngle+','+yawAngle+'\n')
		print([rollAngle, pitchAngle, yawAngle])

def anglePlot(angleData):
	angleData.close()
	
	roll, pitch, yaw = np.loadtxt(angleData, delimiter=',', unpack=True)
	angles = [roll, pitch, yaw]

	anglePlot = chart.figure()
	anglePlots = []

	for i in range(0,3):
		anglePlots.append(anglePlot.add_subplot(3, 1, i))
		anglePlots[i].plot(angles[i])
		chart.grid()
	
	chart.show()

