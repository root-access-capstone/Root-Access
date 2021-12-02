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

def checkIfPumpNeeded(moisture: int, moistureLow: int, board: serial.Serial, floatFlag) -> None:
    """
    Real simple function to check if the pump is needed or not, then turns it on or off accordingly

    :param moisture: The moisture level read from the sensor
    :param moistureLow: The lowest we allow the moisture to go
    :param board: The board from arduinoDriver
    """
    if floatFlag == 'HIGH':
        if(moisture < moistureLow):
            turnPumpOn(board)
        else:
            turnPumpOff(board)
    else:
        turnPumpOff(board)
