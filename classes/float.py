from dataclasses import dataclass


@dataclass
class FloatSensor:
    """Class for handling float flag"""
    flag: bool = False

    def set_low(self):
        """Sets the flag to False"""
        self.flag = False

    def set_high(self):
        """Sets the flag to True"""
        self.flag = True
