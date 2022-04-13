import logging


class Board():
    def __init__(self):
        self.signal = None

    def write(self, bytes):
        """Receives write func from determineSignalToSend"""
        logging.debug(" Board wrote %s",
            bytes.decode("utf-8"))
        self.signal = bytes.decode("utf-8")
