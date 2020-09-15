import matplotlib.pyplot as chart
import numpy as np

roll, pitch, yaw = np.loadtxt('anglesData.txt', delimiter=',', unpack = True)
data = [roll, pitch, yaw]

chart.style.use('seaborn-dark')
anglesPlot = chart.figure(figsize = (10,6))
plots = [0, 0, 0]
labels = ['Roll', 'Pitch', 'Yaw']

for i in range(0, 3):
	plots[i] = anglesPlot.add_subplot(3, 1, i+1)
	plots[i].set_ylabel(labels[i])
	plots[i].plot(data[i])

chart.grid()
chart.show()

