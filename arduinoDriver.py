# Third Party
import time
import logging
from datetime import datetime
from serial import Serial

# Proprietary
from controllers.sendEmail import notifyLowWater, notifyWaterFilled
from controllers.sendData import checkIfDataNeedsSent
from controllers.signalArduino import determineSignalToSend
from controllers.database import Database
from classes.data import Data
from classes.peripheral import Lamp, Pump
from classes.float import FloatSensor


logging.basicConfig(level=logging.ERROR,
    filemode="w",
    filename="error_log.log",
)

board = Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = None,
)

# Data comes in as temperature,humidity,moisture,timeLightOn,floatSensor
thrash_flag = True

light_crit_val = 100
moist_crit_val = 400

floatFlag = FloatSensor()
lamp = Lamp(critical_value=light_crit_val)
pump = Pump(critical_value=moist_crit_val)
data = Data(
    light_critical_value=light_crit_val,
    moisture_critical_value=moist_crit_val
)

emailSent = False
emailTimestamp = 0

timestamp = None
lastMinuteSent = 1
envId = 1
signalSentBool = False

db = Database()

def checkIfEmailNeeded(floatFlag:FloatSensor, emailTimestamp):
    global emailSent
    currentTime = time.time()
    if currentTime - emailTimestamp > 86400:#86400 seconds in 24 hours
        emailSent = False
    if not floatFlag.flag and not emailSent:
        notifyLowWater(currentTime)
        emailSent = True
        emailTimestamp = time.time()
    if floatFlag.flag and emailSent:
        notifyWaterFilled(currentTime)
        emailSent = False
    return emailTimestamp

try:
    while True:
        try:
            while board.inWaiting() == 0:
                if not data.valid:
                    continue
                # emailTimestamp = checkIfEmailNeeded(floatFlag, emailTimestamp)
                returned = checkIfDataNeedsSent(lastMinuteSent,
                    data, lamp,
                    pump, timestamp, envId, db)
                if returned != lastMinuteSent:
                    lastMinuteSent = returned
                if thrash_flag:
                    lamp.evaluate_need(
                        data.lightArray.getAvg())
                    pump.evaluate_need(
                        data.moistureArray.getAvg(),
                        flag=floatFlag.flag)
                    thrash_flag = False
                if not signalSentBool:
                    determineSignalToSend(pump.is_on, lamp.is_on, board)
                    signalSentBool = True
            timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            output = board.readline().decode('utf-8').strip().split(',')
            if len(output) == 6:
                data.update(
                    temperature=int(output[0]),
                    humidity=int(output[1]),
                    moisture=int(output[2]),
                    light=int(output[3])
                )
                if 'LOW' in output[4]:
                    floatFlag.set_low()
                else:
                    floatFlag.set_high()
                thrash_flag = True
                signalSentBool = False
            else:
                logging.error(" Incomplete board output: %s",
                    output)
                continue
        except Exception as error:
            logging.error(" Error reading board: %s",
                error)
finally:
    determineSignalToSend(False, False, board)
