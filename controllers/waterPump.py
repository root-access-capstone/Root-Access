import serial

def turnPumpOn(board:serial.Serial) -> None:
    """
    Writes to board to turn pump on
    
    :param board: The board from arduinoDriver
    """
    board.write(b'A')

def turnPumpOff(board:serial.Serial) -> None:
    """
    Writes to board to turn pump off
    
    :param board: The board from arduinoDriver
    """
    board.write(b'B')