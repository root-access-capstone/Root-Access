import serial

def turnLightOn(board:serial.Serial) -> None:
    """
    Writes to board to turn pump on
    
    :param board: The board from arduinoDriver
    """
    board.write(b'C')

def turnLightOff(board:serial.Serial) -> None:
    """
    Writes to board to turn pump off
    
    :param board: The board from arduinoDriver
    """
    board.write(b'D')