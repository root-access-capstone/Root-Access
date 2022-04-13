from serial import Serial
import logging

def determineSignalToSend(isPumpOn:bool, isLightOn:bool, board:Serial) -> None:
    """Determines the signal to send to the arduino depending on which
    accessories are on or off"""
    if isPumpOn:
        if isLightOn:
            board.write(b'A')
            logging.debug(" Wrote (both on) to the Arduino")
        else:
            board.write(b'C')
            logging.debug(" Wrote (pump on) to the Arduino")
    else:
        if isLightOn:
            board.write(b'D')
            logging.debug(" Wrote (light on) to the Arduino")
        else:
            board.write(b'B')
            logging.debug(" Wrote (both off) to the Arduino")
