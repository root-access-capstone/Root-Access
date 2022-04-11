import logging
from dataclasses import dataclass
from datetime import datetime, timedelta


def time_diff_to_interval_seconds(time_difference:timedelta) -> float:
    """Converts time difference to # of seconds
    in the interval"""
    # seconds_p_interval = 15*60 # 900 seconds per interval
    diff_seconds = time_difference.seconds
    # interval_time_in_seconds = diff_seconds % seconds_p_interval
    return diff_seconds

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

@dataclass
class Peripheral:
    """Class for handling control & related data of Light & Pump"""
    name: str = "Peripheral"
    is_on: bool = False
    time_turned_on: datetime = None
    time_turned_off: datetime = None
    # Value to turn the peripheral on/off
    critical_value: int = 400

    def set_on(self) -> None:
        """Sets is_on to True and saves time_turned_on"""
        if not self.is_on:
            self.is_on = True
            self.time_turned_on = datetime.now()
            self.time_turned_off = None
            logging.debug(" Set %s on at %s", self.name,
                self.time_turned_on)
        else:
            logging.error(" Cannot set_on %s - already on",
                self.name)

    def set_off(self) -> None:
        """Sets is_on to False and saves time_turned_off"""
        if self.is_on:
            self.is_on = False
            self.time_turned_off = datetime.now()
            logging.debug(" Set %s off at %s",
                self.name, self.time_turned_off)
        else:
            logging.error(" Cannot set_on %s - already off",
                self.name)

    def evaluate_need(self, comparison_val:float, flag=False) -> None:
        """Evaluates if the peripheral should be
        turned on, off, or stay the same"""
        if flag:
            return
        if comparison_val <= self.critical_value and not self.is_on:
            self.set_on()
            logging.debug(" Evaluated to set %s on - %s < %s",
                self.name, comparison_val,
                self.critical_value)
        elif comparison_val > self.critical_value and self.is_on:
            self.set_off()
            logging.debug(" Evaluated to set %s off - %s > %s",
                self.name, comparison_val,
                self.critical_value)
        else:
            logging.debug(" Evaluated to keep %s set to %s",
                self.name, self.is_on)

    def calculate_time_on(self, now:datetime) -> float:
        """Calculates & returns duration of time
        in seconds that the peripheral was set on"""
        # now = datetime.now()
        seconds_diff = None
        # Intervals are every time we store data
        if not self.is_on and self.time_turned_off >= (now - timedelta(minutes=15)):
            # Turned off this interval
            time_difference = self.time_turned_off - self.time_turned_on
            logging.debug(" %s turned off this interval, storing for roughly %s minutes",
                self.name ,time_difference)
            seconds_diff = time_diff_to_interval_seconds(time_difference)
        elif self.is_on:
            # On
            time_difference = now - self.time_turned_on
            logging.debug(" %s is on this interval, storing for roughly %s minutes",
                self.name ,time_difference)
            seconds_diff = time_diff_to_interval_seconds(time_difference)
        else:
            logging.debug(" %s wasn't on this interval, storing 0 seconds",
                self.name)
            seconds_diff = 0
        return seconds_diff

    def new_calc(self, now:datetime):
        """New time calc method in testing"""
        # now = datetime.now()
        seconds_diff = None
        # Intervals are every time we store data
        if self.is_on: # need to test w/ time_turned_off set to None
            if self.time_turned_on.minute//15 == now.minute//15:
                # Turned on this interval, still on
                time_difference = now - self.time_turned_on
                logging.debug(" %s turned on this interval, storing for roughly %s minutes",
                    self.name ,time_difference)
                seconds_diff = time_difference.seconds
            else:
                # Turned on previous interval, still on
                time_difference = timedelta(minutes=15)
                logging.debug(" %s turned on in a previous interval, storing for %s minutes",
                    self.name ,time_difference)
                seconds_diff = time_difference.seconds
        elif self.time_turned_off and self.time_turned_off >= (now - timedelta(minutes=15)):
            if self.time_turned_off.minute//15 == self.time_turned_on.minute//15:
                # Turned on & off this interval
                time_difference = self.time_turned_off - self.time_turned_on
                logging.debug(" %s turned off this interval, storing for roughly %s minutes",
                    self.name, time_difference)
                seconds_diff = time_difference.seconds
            else:
                # Turned on in a previous interval, off this interval
                time_difference = timedelta(minutes=self.time_turned_off.minute % 15)
                logging.debug(" %s turned off this interval, storing for roughly %s minutes",
                    self.name, time_difference)
                seconds_diff = time_difference.seconds
        else:
            # Off this interval and not on recently
            logging.debug(" %s wasn't on this interval, storing 0 seconds",
                self.name)
            seconds_diff = 0
        return seconds_diff
