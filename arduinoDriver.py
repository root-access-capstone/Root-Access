# Third Party
from datetime import datetime
import serial
import time

# Proprietary
from controllers.sendEmail import notifyLowWater, notifyWaterFilled
from controllers.sendData import checkIfDataNeedsSent
from controllers.waterPump import checkIfPumpNeeded
from controllers.lightValue import checkIfLightNeeded
from dataclasses.lightArray import LightArray


board = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = None,
)

# Data comes in as temperature,humidity,moisture,timeLightOn,floatSensor
temp = 0
hum = 0
moisture = 0
timeLightOn = 0 # to be implemented
floatFlag = 'LOW'
emailSent = False
timestamp = 0
pumpBool = True
minMoistureLevel = 520
timeDataCollected = 0
lastMinuteSent = 1
envId = 0
lightArray = LightArray()

def checkIfEmailNeeded(floatFlag, timestamp):
    global emailSent
    currentTime = time.time()
    if(currentTime - timestamp > 86400):#86400 seconds in 24 hours
        emailSent = False
    if(floatFlag == 'LOW' and not emailSent):
        notifyLowWater(currentTime)
        emailSent = True
        timestamp = time.time()
    if(floatFlag == 'HIGH' and emailSent):
        notifyWaterFilled(currentTime)
        emailSent = False
    return timestamp

while True:
    try:
        while(board.inWaiting() == 0):
            if temp != 0 and moisture != 0:
                timestamp = checkIfEmailNeeded(floatFlag, timestamp)
                if pumpBool:
                    checkIfPumpNeeded(moisture, minMoistureLevel, board, floatFlag)
                    pumpBool = False
                if temp != -999:
                    lastMinuteSent = checkIfDataNeedsSent(lastMinuteSent, temp, hum, moisture, timeLightOn, timeDataCollected, envId)
                checkIfLightNeeded(lightArray.getAvg(), board)
    except Exception as error:
        print('**Error reading board: ', error)
    timeDataCollected = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    output = board.readline().decode('utf-8').strip().split(',')
    if len(output) == 5:
        temp = output[0]
        hum = output[1]
        moisture = int (output[2])
        lightArray.add(output[3])
        if('LOW' in output[4]):
            floatFlag = 'LOW'
        else:
            floatFlag = 'HIGH'
        pumpBool = True
        print(output)
    else:
        print("Incomplete board output.")
        continue
