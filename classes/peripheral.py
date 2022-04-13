import logging
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class Peripheral(ABC):
    """Class for handling control & related data of peripherals"""
    def __init__(self, is_on:bool = False,
            time_turned_on:datetime = None,
            time_turned_off:datetime = None,
            interval_seconds_on:int = 0,
            critical_value:int = 400):
        self._is_on = is_on
        self._time_turned_on = time_turned_on
        self._time_turned_off = time_turned_off
        self._interval_seconds_on = interval_seconds_on
        self._critical_value = critical_value

    @abstractmethod
    def __repr__(self):
        """Representation dunder"""

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
    def interval_seconds_on(self) -> int:
        """Tracks total seconds the Lamp has been on this interval"""

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

    @interval_seconds_on.setter
    @abstractmethod
    def interval_seconds_on(self, seconds):
        """Setter method for interval_seconds_on"""

    @abstractmethod
    def evaluate_need(self, comparison_val:int) -> None:
        """Evaluates if peripheral should be on or off"""

    def set_on(self, when:datetime=None) -> None:
        """Edits properties for tracking when it was turned on/off"""
        if not self.is_on:
            if not when: # Unit testing
                when = datetime.now()
            self.is_on = True
            self.time_turned_on = when
            self.time_turned_off = None
        else:
            logging.error(" Cannot set_on - already on")

    def set_off(self, when:datetime=None) -> None:
        """Edits properties for tracking when it was turned on/off"""
        if self.is_on:
            if not when: # Unit testing
                when = datetime.now()
            self.is_on = False
            self.time_turned_off = when
            self.calculate_time_on(when)
        else:
            logging.error(" Cannot set_off - already off")

    def get_interval_seconds_on(self, when:datetime=None) -> int:
        """Gets interval_seconds_on, and calculates how long it's
        been on again if it's currently on"""
        if self.is_on:
            if not when: # Unit testing
                when = datetime.now()
            self.calculate_time_on(when)
        temp = self._interval_seconds_on
        self.interval_seconds_on = 0
        return temp

    def calculate_time_on(self, now:datetime = None) -> None:
        """Calculates & returns duration of time
        in seconds that the peripheral was set on"""
        if not now: # Unit Testing
            now = datetime.now()
        # Intervals are every time we store data
        if self.is_on:
            if self.time_turned_on.minute//15 == now.minute//15:
                # Turned on this interval, still on
                time_difference = now - self.time_turned_on
                logging.debug(" Turned on this interval, storing for roughly %s minutes",
                    time_difference)
                self.interval_seconds_on += time_difference.seconds
            else:
                # Turned on previous interval, still on
                time_difference = timedelta(minutes=15)
                logging.debug(" Turned on in a previous interval, storing for %s minutes",
                    time_difference)
                self.interval_seconds_on += time_difference.seconds
        elif self.time_turned_off and self.time_turned_off >= (now - timedelta(minutes=15)):
            if self.time_turned_off.minute//15 == self.time_turned_on.minute//15:
                # Turned on & off this interval
                time_difference = self.time_turned_off - self.time_turned_on
                logging.debug(" Turned off this interval, storing for roughly %s minutes",
                    time_difference)
                self.interval_seconds_on += time_difference.seconds
            else:
                # Turned on in a previous interval, off this interval
                time_difference = timedelta(minutes=self.time_turned_off.minute % 15)
                logging.debug(" Turned off this interval, storing for roughly %s minutes",
                    time_difference)
                self.interval_seconds_on += time_difference.seconds
        else:
            # Off this interval and not on recently
            logging.debug(" Wasn't on this interval, storing 0 seconds")

class Lamp(Peripheral):
    """Instance of Peripheral for our grow lamp"""

    def __repr__(self):
        return ("="*60+
            "\n\t\t\tLamp\n"+"-"*60+
            f"\n\tIs on:\t\t\t\t{self.is_on}"
            f"\n\tTurned on:\t\t\t{self.time_turned_on}"
            f"\n\tTurned off:\t\t\t{self.time_turned_off}"
            f"\n\tInterval Seconds:\t\t{self.interval_seconds_on}"
            f"\n\tCritical value:\t\t\t{self.critical_value}"
            +"\n"+"="*60)

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
    def interval_seconds_on(self):
        """Tracks total seconds the Lamp has been on this interval"""
        return self._interval_seconds_on

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
            raise ValueError(f" Lamp is_on is already == {value}!")

    @time_turned_on.setter
    def time_turned_on(self, time):
        """Setter for time_turned_on"""
        self._time_turned_on = time

    @time_turned_off.setter
    def time_turned_off(self, time):
        """"Setter method for time_turned_off"""
        self._time_turned_off = time

    @interval_seconds_on.setter
    def interval_seconds_on(self, seconds):
        """Setter method for interval_seconds_on"""
        self._interval_seconds_on = seconds

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

    def __repr__(self):
        return ("="*60+
            "\n\t\tPump\n"+"-"*60+
            f"\n\tIs on:\t\t\t\t{self.is_on}"
            f"\n\tTurned on:\t\t\t{self.time_turned_on}"
            f"\n\tTurned off:\t\t\t{self.time_turned_off}"
            f"\n\tInterval Seconds:\t\t{self.interval_seconds_on}"
            f"\n\tCritical value:\t\t\t{self.critical_value}"
            +"\n"+"="*60)

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
    def interval_seconds_on(self):
        """Tracks total seconds the Pump has been on this interval"""
        return self._interval_seconds_on

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
            raise ValueError(f" Pump is_on is already == {value}!")

    @time_turned_on.setter
    def time_turned_on(self, time):
        """Setter for time_turned_on"""
        self._time_turned_on = time

    @time_turned_off.setter
    def time_turned_off(self, time):
        """"Setter method for time_turned_off"""
        self._time_turned_off = time

    @interval_seconds_on.setter
    def interval_seconds_on(self, seconds):
        """Setter method for interval_seconds_on"""
        self._interval_seconds_on = seconds

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
