# Third Party
from datetime import datetime, timedelta
import serial
import time

# Proprietary
from controllers.sendEmail import notifyLowWater, notifyWaterFilled
from controllers.waterPump import turnPumpOff, turnPumpOn
from controllers.lights import turnLightOff, turnLightOn


board = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = None,
)

floatFlag = None
emailSent = False
emailTimeStamp = 0
pumpTimeStamps = [(datetime.now()+timedelta(hours=6*i)).strftime('%H:%M') for i in range(4)]
pumpOnTime = None
print(pumpTimeStamps)
lightTimeStamp = datetime.now().strftime('%H:%M')

def checkIfEmailNeeded(floatFlag, emailTimeStamp):
    global emailSent
    currentTime = time.time()
    if(currentTime - emailTimeStamp > 86400):#86400 seconds in 24 hours
        emailSent = False
    if(floatFlag == 'LOW' and not emailSent):
        notifyLowWater(currentTime)
        emailSent = True
        emailTimeStamp = time.time()
    if(floatFlag == 'HIGH' and emailSent):
        notifyWaterFilled(currentTime)
        emailSent = False
    return emailTimeStamp

while True:
    try:
        while board.inWaiting() == 0:
            emailTimeStamp = checkIfEmailNeeded(floatFlag, emailTimeStamp)
            now = datetime.now().strftime('%H:%M')
            earlierNow = (datetime.now()-timedelta(seconds=10)).strftime('%H:%M:%S')
            if now == lightTimeStamp+timedelta(hours=6):
                turnLightOff(board)
            if lightTimeStamp == now:
                lightOnTime = datetime.now()
                turnLightOn(board)
            if pumpOnTime:
                if datetime.now()  >= pumpOnTime + timedelta(seconds=10):
                    turnPumpOff(board)
                    pumpOnTime = None
            if now in pumpTimeStamps:
                pumpOnTime = datetime.now()
                turnPumpOn(board)
        output = board.readline().decode('utf-8').strip().split(',')
        if len(output) == 1:
            if('LOW' in output[0]):
                floatFlag = 'LOW'
            else:
                floatFlag = 'HIGH'
            pumpBool = True
            print(output)
    except Exception as error:
        print('**Error reading board: ', error)
    else:
        print("Incomplete board output.")
        continue
