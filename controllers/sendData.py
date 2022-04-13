# Third Party
from datetime import datetime
import logging

# Proprietary
from controllers.database import Database, SensorData, new_data_object
from controllers.powerConsumption import measurePowerConsumption
from controllers.waterConsumption import measureWaterConsumption
from classes.data import Data
from classes.peripheral import Lamp, Pump


def checkIfDataNeedsSent(lastMinuteSent, data:Data, lamp:Lamp,
        pump:Pump, timestamp, envId, db) -> datetime.minute:
    """If the time is right (every 15 minutes), calls send_data"""
    minutesToSendOn = [0, 15, 30, 45]
    now = datetime.now()
    minute = now.minute
    if minute in minutesToSendOn:
        if minute != lastMinuteSent:
            pumpOnTime = pump.get_interval_seconds_on()
            lampOnTime = lamp.get_interval_seconds_on()
            moisture = data.moistureArray.getAvg()
            kwh = measurePowerConsumption(
                pumpOnTime, lampOnTime)
            ml = measureWaterConsumption(
                pumpOnTime)
            data_string = (f"{envId},{timestamp},{lampOnTime},"
                f"{ml},{kwh},{data.humidity},{moisture},"
                f"{data.temperature}")
            logging.debug(" Sending data string: \n\t%s",
                data_string)
            send_data(data_string, db)
            lastMinuteSent = minute
    return lastMinuteSent

def send_data(data:str, db:Database) -> bool:
    """Sends data to database.
    Returns 1 if success, 0 otherwise."""
    data = new_data_object(data)
    try:
        db.Session.add(data)
        db.Session.commit()
        result = db.Session.query(SensorData).all()
        if result:
            logging.info(' Stored sensor data in database.')
        else:
            logging.error(' Failed to query database.')
    except Exception as error:
        logging.error(' Error adding to or querying database: %s',
            error)
        return 0
    return 1
