from datetime import datetime
from time import time_ns

from send_record import send_record

def checkIfDataNeedsSent(lastMinuteSent, temp, hum, moisture, timeLightOn, timestamp, envId):
	minutesToSendOn = [0, 15, 30, 45]
	now = datetime.now()
	minute = now.minute
	if minute in minutesToSendOn:
		if minute != lastMinuteSent:
			inputDict = {
				'topic': 'sensor_data',
				'record_value': f'{envId},{timestamp},,{hum},{moisture},{temp},'
			}
			send_record(inputDict)
			lastMinuteSent = minute
	return lastMinuteSent