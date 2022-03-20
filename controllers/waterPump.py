import serial
from datetime import datetime

# def turnPumpOn(board:serial.Serial) -> None:
#     """
#     Writes to board to turn pump on
    
#     :param board: The board from arduinoDriver
#     """
#     board.write(b'A')

# def turnPumpOff(board:serial.Serial) -> None:
#     """
#     Writes to board to turn pump off
    
#     :param board: The board from arduinoDriver
#     """
#     board.write(b'B')

def checkIfPumpNeeded(moisture: int, moistureHigh: int, floatFlag:str, pumpStartTime:int, isPumpOn:bool) -> tuple:
    """
    Real simple function to check if the pump is needed or not, then turns it on or off accordingly

    :param moisture: The moisture level read from the sensor
    :param moistureHigh: The lowest we allow the moisture to go
    :param floatFlag: Flag indicating if we have enough water in the reservoir
    :param pumpStartTime: The time the pump turned on
    :param isPumpOn: Flag indicating if the pump is on or off
    """
    if floatFlag == 'HIGH':
        if isPumpOn:#Pump is on, keep on
            if moisture > moistureHigh:
                # turnPumpOn(board)
                return pumpStartTime, isPumpOn, False
            else:#pump is on, turn off
                # turnPumpOff(board)
                return pumpStartTime, False, True
        else:
            if moisture > moistureHigh:#pump is off, turn on
                # turnPumpOn(board)
                return datetime.now(), True, False
            else:
                # turnPumpOff(board) #pump is off, keep off
                return pumpStartTime, isPumpOn, False
    else:
        # turnPumpOff(board)
        if isPumpOn:
            return pumpStartTime, False, True
        else:
            return pumpStartTime, isPumpOn, False

