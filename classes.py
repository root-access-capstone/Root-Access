import logging
from dataclasses import dataclass
from datetime import datetime, timedelta


def time_diff_to_interval_seconds(time_difference:timedelta) -> float:
    """Converts time difference to # of seconds in the interval"""
    seconds_p_interval = 15*60 # 900 seconds per interval
    diff_seconds = time_difference.seconds
    interval_time_in_seconds = diff_seconds % seconds_p_interval
    return interval_time_in_seconds

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
class LightFixture:
    """Class for handling light fixture & related data"""
    is_on: bool = False
    time_turned_on: datetime = None
    time_turned_off: datetime = None
    duration_on: timedelta = timedelta(seconds=0)
    critical_value: int = 100 # Value to turn the light on/off
    def set_on(self):
        """Sets is_on to True and saves time_turned_on"""
        if not self.is_on:
            self.is_on = True
            self.time_turned_on = datetime.now()
            self.time_turned_off = None
            logging.debug(" Set LightFixture on at %s", self.time_turned_on)
        else:
            logging.error(" Cannot set_on LightFixture - already on")

    def set_off(self):
        """Sets is_on to False and saves time_turned_off"""
        if self.is_on:
            self.is_on = False
            self.time_turned_off = datetime.now()
            logging.debug(" Set LightFixture off at %s", self.time_turned_off)
        else:
            logging.error(" Cannot set_off LightFixture - already off")

    def evaluate_need(self, light_avg:float):
        """Evaluates if the light should be turned on, off, or stay the same"""
        if light_avg <= self.critical_value and not self.is_on:
            self.set_on()
            logging.debug(" Evaluated to set LightFixture on for light value %s", light_avg)
        elif light_avg > self.critical_value and self.is_on:
            self.set_off()
            logging.debug(" Evaluated to set LightFixture off for light value %s", light_avg)

    def calculate_time_on(self):
        """Calculates duration of time in seconds that LightFixture was set on"""
        now = datetime.now()
        # Intervals are every time we store data
        if not self.is_on and self.time_turned_off >= (now - timedelta(minutes=15)):
            # Turned off this interval
            time_difference = self.time_turned_off - self.time_turned_on
            logging.debug(" Light turned off this interval, storing for roughly %s minutes",
                time_difference)
            return time_diff_to_interval_seconds(time_difference)
        elif self.is_on:
            # On
            time_difference = now - self.time_turned_on
            logging.debug(" Light is on this interval, storing for roughly %s minutes",
                time_difference)
            return time_diff_to_interval_seconds(time_difference)
        else:
            logging.debug(" Light wasn't on this interval, storing 0 seconds")
            return timedelta(seconds=0)
