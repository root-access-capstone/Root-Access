# Third Party
from datetime import datetime

# Proprietary
from data_to_mysql import send_data


def checkIfDataNeedsSent(lastMinuteSent, temp, hum, moisture, timeLightOn, timestamp, envId) -> None:
    """If the time is right (every 15 minutes), calls send_data"""
    minutesToSendOn = [0, 15, 30, 45]
    now = datetime.now()
    minute = now.minute
    if minute in minutesToSendOn:
        if minute != lastMinuteSent:
            send_data(f'{envId},{timestamp},{timeLightOn},{hum},{moisture},{temp},{envId}')
            lastMinuteSent = minute
    return lastMinuteSent
