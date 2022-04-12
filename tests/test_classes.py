from datetime import datetime, timedelta
import logging

from classes import Light, Pump


logging.basicConfig(level=logging.DEBUG)

def test_light_set_on():
    """Tests the Light's set_on method"""
    light = Light()
    light.set_on()
    assert light.is_on is True
    assert light.time_turned_on.strftime('%H:%M:%S') == datetime.now().strftime('%H:%M:%S')
    assert light.time_turned_off is None

def test_light_set_off():
    """Tests the Light's set_off method"""
    five_mins_ago = datetime.now() - timedelta(minutes=5)
    light = Light(is_on=True, time_turned_on=five_mins_ago)
    light.set_off()
    assert light.is_on is False
    assert light.time_turned_off.strftime('%H:%M:%S') == datetime.now().strftime('%H:%M:%S')

def test_pump_set_on():
    """Tests the Pump's set_on method"""
    pump = Pump()
    pump.set_on()
    assert pump.is_on is True
    assert pump.time_turned_on.strftime('%H:%M:%S') == datetime.now().strftime('%H:%M:%S')
    assert pump.time_turned_off is None

def test_pump_set_off():
    """Tests the Pump's set_off method"""
    five_mins_ago = datetime.now() - timedelta(minutes=5)
    pump = Pump(is_on=True, time_turned_on=five_mins_ago)
    pump.set_off()
    assert pump.is_on is False
    assert pump.time_turned_off.strftime('%H:%M:%S') == datetime.now().strftime('%H:%M:%S')

def test_light_evaluate_need_below():
    """Tests the Light's light_evaluate_need method
    when it should be turned on"""
    light = Light(critical_value=10)
    light.evaluate_need(5)
    assert light.is_on is True

def test_light_evaluate_need_above():
    """Tests the Light's light_evaluate_need method
    when it should be turned off"""
    light = Light(critical_value=10)
    light.evaluate_need(15)
    assert light.is_on is False

def test_pump_evaluate_need_below():
    """Tests the Pump's pump_evaluate_need method
    when it should be turned off"""
    pump = Pump(critical_value=10)
    pump.evaluate_need(5)
    assert pump.is_on is False

def test_pump_evaluate_need_above():
    """Tests the Pump's pump_evaluate_need method
    when it should be turned off"""
    pump = Pump(critical_value=10)
    pump.evaluate_need(15)
    assert pump.is_on is True

def test_calc_time_on_same_interval():
    """Tests the Light's calculate_time_on method
    when turned on in the current interval"""
    now = datetime(2022,4,11,9,29,56)
    five_mins_ago = now - timedelta(minutes=5)
    five_mins_seconds = 5 * 60
    light = Light(is_on=True, time_turned_on=five_mins_ago)
    assert light.calculate_time_on(now) == five_mins_seconds

def test_calc_time_on_diff_interval():
    """Tests the Light's calculate_time_on method
    when turned on in a previous interval"""
    now = datetime(2022,4,11,9,29,56)
    twenty_mins_ago = now - timedelta(minutes=20)
    interval_seconds = 15 * 60
    light = Light(is_on=True, time_turned_on=twenty_mins_ago)
    assert light.calculate_time_on(now) == interval_seconds

def test_calc_time_off_same_interval():
    """Tests the Light's calculate_time_on method
    when off but turned on the same interval"""
    now = datetime(2022,4,11,9,29,56)
    seven_mins_ago = now - timedelta(minutes=7)
    five_mins_ago = now - timedelta(minutes=5)
    two_mins_seconds = 2 * 60
    light = Light(is_on=False, time_turned_on=seven_mins_ago,
        time_turned_off=five_mins_ago)
    assert light.calculate_time_on(now) == two_mins_seconds

def test_calc_time_off_diff_interval():
    """Tests the Light's calculate_time_on method
    when off but turned on in previous interval"""
    now = datetime(2022,4,11,9,29,56)
    twenty_mins_ago = now - timedelta(minutes=20)
    five_mins_ago = now - timedelta(minutes=5)
    nine_mins_seconds = 9 * 60
    light = Light(is_on=False, time_turned_on=twenty_mins_ago,
        time_turned_off=five_mins_ago)
    assert light.calculate_time_on(now) == nine_mins_seconds
