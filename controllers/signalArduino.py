import serial

def determineSignalToSend(isPumpOn:bool, isLightOn:bool, board:serial.Serial):
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