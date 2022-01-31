# Third Party
from datetime import datetime

# Proprietary
from controllers.database import Database, SensorData, new_data_object
from controllers.powerConsumption import measurePowerConsumption
from controllers.waterConsumption import measureWaterConsumption

def checkIfDataNeedsSent(lastMinuteSent, temp, hum, moisture, timeLightOn, timePumpOn, timestamp, envId) -> None:
    """If the time is right (every 15 minutes), calls send_data"""
    minutesToSendOn = [0, 15, 30, 45]
    now = datetime.now()
    minute = now.minute
    if minute in minutesToSendOn:
        if minute != lastMinuteSent:
            kwh = measurePowerConsumption(timePumpOn, timeLightOn)
            ml = measureWaterConsumption(timePumpOn)
            send_data(f'{envId},{timestamp},{timeLightOn},{ml},{kwh},{hum},{moisture},{temp}')
            lastMinuteSent = minute
    return lastMinuteSent

def send_data(data:str) -> bool:
    """Sends data to database.
    Returns 1 if success, 0 otherwise."""
    db = Database()
    data = new_data_object(data)
    try:
        db.Session.add(data)
        db.Session.commit()
        result = db.Session.query(SensorData).all()
        db.Session.close()
        if result:
            print('Stored sensor data in database.')
        else:
            print('** Error: Failed to query database.')
    except Exception as error:
        print('**Error adding to or querying database: ', error)
        return 0
    return 1

if __name__ == '__main__':
    incoming = '0,2021-04-22 02:22:22,2,4,100,10,3'
    result = send_data(incoming)
    assert result, "Failed to send data."
