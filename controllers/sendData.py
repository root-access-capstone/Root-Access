from datetime import datetime

def checkIfDataNeedsSent(lastMinuteSent):
	minutesToSendOn = [0, 15, 30, 45]
	now = datetime.now()
	minute = now.minute
	if minute in minutesToSendOn:
		if minute != lastMinuteSent:
			return True