# Proprietary
from data_to_mysql import send_data

# Third Party
from datetime import datetime


def checkIfDataNeedsSent(lastMinuteSent, temp, hum, moisture, timeLightOn, timestamp, envId):
	minutesToSendOn = [0, 15, 30, 45]
	now = datetime.now()
	minute = now.minute
	if minute in minutesToSendOn:
		if minute != lastMinuteSent:
			send_data(f'{envId},{timestamp},0,{hum},{moisture},{temp},0')
			lastMinuteSent = minute
	return lastMinuteSent