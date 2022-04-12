import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from time import sleep


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

class Peripheral(ABC):
    """Class for handling control & related data of peripherals"""
    def __init__(self, is_on:bool = False,
            time_turned_on:datetime = None,
            time_turned_off:datetime = None,
            critical_value:int = 400):
        self._is_on = is_on
        self._time_turned_on = time_turned_on
        self._time_turned_off = time_turned_off
        self._critical_value = critical_value

    @property
    @abstractmethod
    def is_on(self) -> bool:
        """Property for whether the peripheral is on/off"""

    @property
    @abstractmethod
    def time_turned_on(self) -> datetime:
        """Tracks time the peripheral was turned on"""

    @property
    @abstractmethod
    def time_turned_off(self) -> datetime:
        """Tracks time the peripheral was turned off"""

    @property
    @abstractmethod
    def critical_value(self) -> int:
        """Value we use to evaluate the need of peripheral"""

    @is_on.setter
    @abstractmethod
    def is_on(self, value:bool):
        """Setter for is_on"""
        if not self._is_on is value:
            self._is_on = value
            logging.debug(" Set is_on = %s",
                value)
        else:
            raise ValueError(f" is_on is already == {value}!")

    @time_turned_on.setter
    @abstractmethod
    def time_turned_on(self):
        """Setter for time_turned_on"""

    @time_turned_off.setter
    @abstractmethod
    def time_turned_off(self):
        """"Setter method for time_turned_off"""

    @abstractmethod
    def evaluate_need(self, comparison_val:int) -> None:
        """Evaluates if peripheral should be on or off"""

    def set_on(self) -> None:
        """Edits properties for tracking when it was turned on/off"""
        if not self.is_on:
            self.is_on = True
            self.time_turned_on = datetime.now()
            self.time_turned_off = None
        else:
            logging.error(" Cannot set_on - already on")

    def set_off(self) -> None:
        """Edits properties for tracking when it was turned on/off"""
        if self.is_on:
            self.is_on = False
            self.time_turned_off = datetime.now()
        else:
            logging.error(" Cannot set_off - already off")

    def calculate_time_on(self, now:datetime = None) -> int:
        """Calculates & returns duration of time
        in seconds that the peripheral was set on"""
        if not now: # for Unit Testing
            now = datetime.now()
        seconds_diff = None
        # Intervals are every time we store data
        if self.is_on:
            if self.time_turned_on.minute//15 == now.minute//15:
                # Turned on this interval, still on
                time_difference = now - self.time_turned_on
                logging.debug(" Turned on this interval, storing for roughly %s minutes",
                    time_difference)
                seconds_diff = time_difference.seconds
            else:
                # Turned on previous interval, still on
                time_difference = timedelta(minutes=15)
                logging.debug(" Turned on in a previous interval, storing for %s minutes",
                    time_difference)
                seconds_diff = time_difference.seconds
        elif self.time_turned_off and self.time_turned_off >= (now - timedelta(minutes=15)):
            if self.time_turned_off.minute//15 == self.time_turned_on.minute//15:
                # Turned on & off this interval
                time_difference = self.time_turned_off - self.time_turned_on
                logging.debug(" Turned off this interval, storing for roughly %s minutes",
                    time_difference)
                seconds_diff = time_difference.seconds
            else:
                # Turned on in a previous interval, off this interval
                time_difference = timedelta(minutes=self.time_turned_off.minute % 15)
                logging.debug(" Turned off this interval, storing for roughly %s minutes",
                    time_difference)
                seconds_diff = time_difference.seconds
        else:
            # Off this interval and not on recently
            logging.debug(" Wasn't on this interval, storing 0 seconds")
            seconds_diff = 0
        return seconds_diff

class Lamp(Peripheral):
    """Instance of Peripheral for our grow lamp"""

    @property
    def is_on(self):
        """Property for whether the Lamp is on/off"""
        return self._is_on

    @property
    def time_turned_on(self):
        """Tracks time the Lamp was turned on"""
        return self._time_turned_on

    @property
    def time_turned_off(self):
        """Tracks time the Lamp was turned off"""
        return self._time_turned_off

    @property
    def critical_value(self):
        """Value we use to evaluate the need of Lamp"""
        return self._critical_value

    @is_on.setter
    def is_on(self, value:bool):
        """Setter for is_on"""
        if not self._is_on is value:
            self._is_on = value
            logging.debug(" Set is_on = %s",
                value)
        else:
            raise ValueError(f" is_on is already == {value}!")

    @time_turned_on.setter
    def time_turned_on(self, time):
        """Setter for time_turned_on"""
        self._time_turned_on = time

    @time_turned_off.setter
    def time_turned_off(self, time):
        """"Setter method for time_turned_off"""
        self._time_turned_off = time

    def evaluate_need(self, comparison_val:int):
        """Evaluates if Lamp should be on or off"""
        logging.debug(" Evaluating Lamp - %s vs %s",
                comparison_val, self.critical_value)
        if comparison_val <= self.critical_value and not self.is_on:
            self.set_on()
        elif comparison_val > self.critical_value and self.is_on:
            self.set_off()
        else:
            return

class Pump(Peripheral):
    """Instance of Peripheral for our Pump"""

    @property
    def is_on(self):
        """Property for whether the Pump is on/off"""
        return self._is_on

    @property
    def time_turned_on(self):
        """Tracks time the Pump was turned on"""
        return self._time_turned_on

    @property
    def time_turned_off(self):
        """Tracks time the Pump was turned off"""
        return self._time_turned_off

    @property
    def critical_value(self):
        """Value we use to evaluate the need of Pump"""
        return self._critical_value

    @is_on.setter
    def is_on(self, value:bool):
        """Setter for is_on"""
        if not self._is_on is value:
            self._is_on = value
            logging.debug(" Set is_on = %s",
                value)
        else:
            raise ValueError(f" is_on is already == {value}!")

    @time_turned_on.setter
    def time_turned_on(self, time):
        """Setter for time_turned_on"""
        self._time_turned_on = time

    @time_turned_off.setter
    def time_turned_off(self, time):
        """"Setter method for time_turned_off"""
        self._time_turned_off = time

    def evaluate_need(self, comparison_val:int, flag:bool = True):
        """Evaluates if Pump should be on or off - flag is the FloatSensor"""
        logging.debug(" Evaluating Pump - %s vs %s",
                comparison_val, self.critical_value)
        if not flag:
            return
        if comparison_val >= self.critical_value and not self.is_on:
            self.set_on()
        elif comparison_val < self.critical_value and self.is_on:
            self.set_off()
        else:
            return

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    per = Pump(critical_value=3)
    for i in range(1,6):
        sleep(2)
        per.evaluate_need(i, True)
