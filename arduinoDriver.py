from datetime import datetime
import serial
import time

from controllers.email import notifyLowWater, notifyWaterFilled
from controllers.sendData import checkIfDataNeedsSent
from controllers.waterPump import checkIfPumpNeeded


board = serial.Serial(
	port = 'COM3',
	baudrate = 115200,
	timeout = None,
)

# Data comes in as temperature,humidity,moisture,light,floatSensor
temp = 0
hum = 0
moisture = 0
light = 0
floatFlag = False
emailSent = False
timestamp = 0
pumpBool = True
minMoistureLevel = 520
timeDataCollected = 0
lastMinuteSent = 1
envId = 0
def checkIfEmailNeeded(temp, hum, moisture, light, floatFlag, timestamp):
	currentTime = time.time()
	if(currentTime - timestamp > 86400):#86400 seconds in 24 hours
		emailSent = False
	# print(temp, hum, moisture, light, floatFlag)
	# print(f'Email sent {emailSent}')
	if(floatFlag == 'LOW' and not emailSent):
		notifyLowWater(currentTime)
		emailSent = True
		timestamp = time.time()
	if(floatFlag == 'HIGH' and emailSent):
		notifyWaterFilled(currentTime)
		emailSent = False

while True:
	while(board.inWaiting() == 0):
		checkIfEmailNeeded(temp, hum, moisture, light, floatFlag, timestamp)
		if pumpBool:
			checkIfPumpNeeded(moisture, minMoistureLevel, board, floatFlag)
			pumpBool = False
		lastMinuteSent = checkIfDataNeedsSent(lastMinuteSent, temp, hum, moisture, None, timeDataCollected, 'endId')
	timeDataCollected = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
	output = board.readline().decode('utf-8').strip().split(',')
	print(output)
	temp = output[0]
	hum = output[1]
	moisture = int (output[2])
	light = output[3]
	if('LOW' in output[4]):
		floatFlag = 'LOW'
	else:
		floatFlag = 'HIGH'
	pumpBool = True