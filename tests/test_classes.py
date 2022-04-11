from datetime import datetime, timedelta
import logging

from classes import Peripheral


logging.basicConfig(level=logging.DEBUG)

def test_set_on():
    """Tests the Peripheral's set_on method"""
    peripheral = Peripheral()
    peripheral.set_on()
    assert peripheral.is_on is True
    assert peripheral.time_turned_on.strftime('%H:%M:%S') == datetime.now().strftime('%H:%M:%S')
    assert peripheral.time_turned_off is None

def test_set_off():
    """Tests the Peripheral's set_off method"""
    five_mins_ago = datetime.now() - timedelta(minutes=5)
    peripheral = Peripheral(is_on=True, time_turned_on=five_mins_ago)
    peripheral.set_off()
    assert peripheral.is_on is False
    assert peripheral.time_turned_off.strftime('%H:%M:%S') == datetime.now().strftime('%H:%M:%S')

def test_evaluate_need_below():
    """Tests the Peripheral's evaluate_need method
    when it should be turned on"""
    peripheral = Peripheral(critical_value=10)
    peripheral.evaluate_need(5)
    assert peripheral.is_on is True

def test_evaluate_need_above():
    """Tests the Peripheral's evaluate_need method
    when it should be turned off"""
    peripheral = Peripheral(critical_value=10)
    peripheral.evaluate_need(15)
    assert peripheral.is_on is False

def test_calc_time_on_same_interval():
    """Tests the Peripheral's calculate_time_on method
    when turned on in the current interval"""
    now = datetime(2022,4,11,9,29,56)
    five_mins_ago = now - timedelta(minutes=5)
    five_mins_seconds = 5 * 60
    peripheral = Peripheral(is_on=True, time_turned_on=five_mins_ago)
    assert peripheral.calculate_time_on(now) == five_mins_seconds

def test_calc_time_on_diff_interval():
    """Tests the Peripheral's calculate_time_on method
    when turned on in a previous interval"""
    now = datetime(2022,4,11,9,29,56)
    twenty_mins_ago = now - timedelta(minutes=20)
    interval_seconds = 15 * 60
    peripheral = Peripheral(is_on=True, time_turned_on=twenty_mins_ago)
    assert peripheral.calculate_time_on(now) == interval_seconds

def test_calc_time_off_same_interval():
    """Tests the Peripheral's calculate_time_on method
    when off but turned on the same interval"""
    now = datetime(2022,4,11,9,29,56)
    seven_mins_ago = now - timedelta(minutes=7)
    five_mins_ago = now - timedelta(minutes=5)
    two_mins_seconds = 2 * 60
    peripheral = Peripheral(is_on=False, time_turned_on=seven_mins_ago,
        time_turned_off=five_mins_ago)
    assert peripheral.calculate_time_on(now) == two_mins_seconds

def test_calc_time_off_diff_interval():
    """Tests the Peripheral's calculate_time_on method
    when off but turned on in previous interval"""
    now = datetime(2022,4,11,9,29,56)
    twenty_mins_ago = now - timedelta(minutes=20)
    five_mins_ago = now - timedelta(minutes=5)
    nine_mins_seconds = 9 * 60
    peripheral = Peripheral(is_on=False, time_turned_on=twenty_mins_ago,
        time_turned_off=five_mins_ago)
    assert peripheral.calculate_time_on(now) == nine_mins_seconds
