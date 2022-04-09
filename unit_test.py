from classes import LightFixture, Peripheral
from controllers.lightValue import calculateLightTimeOn, checkIfLightNeeded
from controllers.dataArray import DataArray
from datetime import datetime, timedelta
import logging


logging.basicConfig(level=logging.DEBUG)

light_on = datetime.now() - timedelta(minutes=5)
light_off = light_on + timedelta(minutes=3)

light_fixt = Peripheral(
    name="Light",
    time_turned_on=light_on,
    time_turned_off=light_off,
    critical_value=100,
    # is_on=True
)

pump = Peripheral(
    name="Pump",
    time_turned_on=light_on,
    # time_turned_off=light_off,
    critical_value=400,
    is_on=True
)

lightStartOn = 0
timeLightOn = 0
isLightOn = False
lightBool = True
lightOn = False

lightArray = DataArray(80, 20)
moistArray = DataArray(500, 20)

def compare_need():
    global lightStartOn, isLightOn, endTime, lightArray

    lightStartOn, isLightOn, endTime = checkIfLightNeeded(lightArray.getAvg(), lightStartOn, isLightOn)

    print("="*60)
    print("Old func start time: ",lightStartOn)
    print("Old func is on: ",isLightOn)
    print("Old func end time: ",endTime)

    print("-"*60)
    light_fixt.evaluate_need(lightArray.getAvg())
    print("New func start time: ",light_fixt.time_turned_on)
    print("New func is on: ",light_fixt.is_on)
    print("New func end time: ",light_fixt.time_turned_off)

    print("-"*60)
    pump.evaluate_need(moistArray.getAvg())
    print("New func start time: ",pump.time_turned_on)
    print("New func is on: ",pump.is_on)
    print("New func end time: ",pump.time_turned_off)

def compare_time_on():
    global light_fixt
    print("="*60)
    print(calculateLightTimeOn(light_on), "minutes")

    print("-"*60)
    print(light_fixt.calculate_time_on(), "seconds")

    print("-"*60)
    print(pump.calculate_time_on(), "seconds")

if __name__ == "__main__":
    compare_time_on()
    compare_need()
