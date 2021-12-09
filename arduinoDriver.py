# Third Party
from datetime import datetime
import serial
import time

# Proprietary
from controllers.sendEmail import notifyLowWater, notifyWaterFilled
from controllers.sendData import checkIfDataNeedsSent
from controllers.signalArduino import determineSignalToSend
from controllers.waterPump import checkIfPumpNeeded
from controllers.lightValue import checkIfLightNeeded
from controllers.lightArray import LightArray


board = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = None,
)

# Data comes in as temperature,humidity,moisture,timeLightOn,floatSensor
temp = 0
hum = 0
moisture = 0

lightStartOn = 0
timeLightOn = 0
isLightOn = False
lightBool = True
lightOn = False
lightArray = LightArray(30)

pumpStartOn = 0
timePumpOn = 0
isPumpOn = False
pumpBool = True

floatFlag = 'LOW'
emailSent = False
emailTimestamp = 0

moistureHigh = 450
timeDataCollected = 0
lastMinuteSent = 1
envId = 1

def checkIfEmailNeeded(floatFlag, emailTimestamp):
    global emailSent
    currentTime = time.time()
    if(currentTime - emailTimestamp > 86400):#86400 seconds in 24 hours
        emailSent = False
    if(floatFlag == 'LOW' and not emailSent):
        notifyLowWater(currentTime)
        emailSent = True
        emailTimestamp = time.time()
    if(floatFlag == 'HIGH' and emailSent):
        notifyWaterFilled(currentTime)
        emailSent = False
    return emailTimestamp

while True:
    try:
        while(board.inWaiting() == 0):
            if temp != 0 and moisture != 0:
                emailTimestamp = checkIfEmailNeeded(floatFlag, emailTimestamp)
                if pumpBool:
                    pumpStartOn, isPumpOn, endTime = checkIfPumpNeeded(moisture, moistureHigh, floatFlag, pumpStartOn, isPumpOn)
                    if endTime:
                        timePumpOn += int((datetime.now() - pumpStartOn).total_seconds()/60)
                    pumpBool = False
                if temp != -999:
                    returned = checkIfDataNeedsSent(lastMinuteSent, temp, hum, moisture, timeLightOn, timePumpOn, timeDataCollected, envId)
                    if returned != lastMinuteSent:
                        lastMinuteSent = returned
                        timeLightOn = 0
                        timePumpOn = 0
                if lightBool:
                    lightStartOn, isLightOn, endTime = checkIfLightNeeded(lightArray.getAvg(), lightStartOn, isLightOn)
                    if endTime:
                        timeLightOn += int((datetime.now() - lightStartOn).total_seconds()/60)
                    lightBool = False
                determineSignalToSend(isPumpOn, isLightOn, board)
        timeDataCollected = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        output = board.readline().decode('utf-8').strip().split(',')
        if len(output) == 6:
            temp = output[0]
            hum = output[1]
            moisture = int (output[2])
            lightArray.add(output[3])
            if 'LOW' in output[4]:
                floatFlag = 'LOW'
            else:
                floatFlag = 'HIGH'
            pumpBool = True
            lightBool = True
            print(output)
        else:
            print("Incomplete board output.")
            continue
    except Exception as error:
        print('**Error reading board: ', error)
