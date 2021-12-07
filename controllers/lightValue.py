import serial

def turnLightOn(board:serial.Serial) -> None:
    """
    Writes to board to turn light on

    :param board: The board from arduinoDriver
    """
    board.write(b'C')

def turnLightOff(board:serial.Serial) -> None:
    """
    Writes to board to turn light off

    :param board: The board from arduinoDriver
    """
    board.write(b'D')

def checkIfLightNeeded(avg:int, board:serial.Serial) -> None:
    """
    Checks if the light is needed or not, then turns it
    on or off accordingly.

    :param avg: The average value of the LightArray
    """
    if avg <= 100:
        turnLightOn(board)
    else:
        turnLightOff(board)
