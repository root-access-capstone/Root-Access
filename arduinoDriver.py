# Third Party
from datetime import datetime
import serial
import time
import logging

# Proprietary
from controllers.sendEmail import notifyLowWater, notifyWaterFilled
from controllers.sendData import checkIfDataNeedsSent
from controllers.signalArduino import determineSignalToSend
from controllers.dataArray import DataArray
from controllers.database import Database

from classes import FloatSensor, Lamp, Pump


logging.basicConfig(level=logging.ERROR,
    filemode="w",
    filename="error_log.log",
)

board = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = None,
)

# Data comes in as temperature,humidity,moisture,timeLightOn,floatSensor
temp = 0
hum = 0
moisture = 0

thrash_flag = True

lightArray = DataArray(101, 20)
moistureArray = DataArray(450, 5)

lamp = Lamp(critical_value=100)
pump = Pump(critical_value=400)

floatFlag = FloatSensor()
emailSent = False
emailTimestamp = 0

timeDataCollected = 0
lastMinuteSent = 1
envId = 1
signalSentBool = False

db = Database()

def checkIfEmailNeeded(floatFlag:FloatSensor, emailTimestamp):
    global emailSent
    currentTime = time.time()
    if(currentTime - emailTimestamp > 86400):#86400 seconds in 24 hours
        emailSent = False
    if not floatFlag.flag and not emailSent:
        notifyLowWater(currentTime)
        emailSent = True
        emailTimestamp = time.time()
    if floatFlag.flag and emailSent:
        notifyWaterFilled(currentTime)
        emailSent = False
    return emailTimestamp

while True:
    try:
        while board.inWaiting() == 0:
            if temp == 0 or temp == -999 or moisture == 0:
                continue
            # emailTimestamp = checkIfEmailNeeded(floatFlag, emailTimestamp)
            returned = checkIfDataNeedsSent(lastMinuteSent, temp, hum, moistureArray.getAvg(),
                lamp.calculate_time_on(), pump.calculate_time_on(), timeDataCollected,
                envId, db)
            if returned != lastMinuteSent:
                lastMinuteSent = returned
            if thrash_flag:
                lamp.evaluate_need(lightArray.getAvg())
                pump.evaluate_need(moistureArray.getAvg(),
                    flag=floatFlag.flag)
                thrash_flag = False
            if not signalSentBool:
                determineSignalToSend(pump.is_on, lamp.is_on, board)
                signalSentBool = True
        timeDataCollected = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        output = board.readline().decode('utf-8').strip().split(',')
        if len(output) == 6:
            temp = output[0]
            hum = output[1]
            moisture = int (output[2])
            moistureArray.add(moisture)
            lightArray.add(output[3])
            if 'LOW' in output[4]:
                floatFlag.set_low()
            else:
                floatFlag.set_high()
            thrash_flag = True
            signalSentBool = False
            print(output)
        else:
            logging.error(" Incomplete board output: %s", output)
            continue
    except Exception as error:
        logging.error(" Error reading board: %s", error)
    finally:
        determineSignalToSend(False, False, board)
