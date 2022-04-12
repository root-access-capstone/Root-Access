from serial import Serial

def determineSignalToSend(isPumpOn:bool, isLightOn:bool, board:Serial) -> None:
    """Determines the signal to send to the arduino depending on which
    accessories are on or off"""
    if isPumpOn:
        if isLightOn:
            board.write(b'A')
        else:
            board.write(b'C')
    else:
        if isLightOn:
            board.write(b'D')
        else:
            board.write(b'B')
