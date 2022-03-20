import serial
from datetime import datetime

# def turnLightOn(board:serial.Serial) -> None:
#     """
#     Writes to board to turn light on

#     :param board: The board from arduinoDriver
#     """
#     board.write(b'C')

# def turnLightOff(board:serial.Serial) -> None:
#     """
#     Writes to board to turn light off

#     :param board: The board from arduinoDriver
#     """
#     board.write(b'D')

def checkIfLightNeeded(avg:int, lightStartTime:int, isLightOn:bool) -> tuple:
    """
    Checks if the light is needed or not, then turns it
    on or off accordingly.

    :param avg: The average value of the LightArray
    :param lightStartTime: Timestamp when the light was turned on
    :param isLightOn: Flag indicating the light being on or off
    """
    if isLightOn:
        if avg <= 100:
            # turnLightOn(board)
            return lightStartTime, isLightOn, False
        else:
            # turnLightOff(board)
            return lightStartTime, False, True
    else:
        if avg <= 100:
            # turnLightOn(board)
            return datetime.now(), True, False
        else:
            # turnLightOff(board)
            return lightStartTime, isLightOn, False