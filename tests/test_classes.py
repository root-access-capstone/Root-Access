import logging
from datetime import datetime, timedelta

from classes.data import Data
from classes.peripheral import Lamp, Pump


logging.basicConfig(level=logging.DEBUG)

def test_lamp_set_on():
    """Tests the Lamp's set_on method"""
    lamp = Lamp()
    lamp.set_on()
    assert lamp.is_on is True
    assert lamp.time_turned_on.strftime('%H:%M:%S') == datetime.now().strftime('%H:%M:%S')
    assert lamp.time_turned_off is None

def test_lamp_set_off():
    """Tests the Lamp's set_off method"""
    five_mins_ago = datetime.now() - timedelta(minutes=5)
    lamp = Lamp(is_on=True, time_turned_on=five_mins_ago)
    lamp.set_off()
    assert lamp.is_on is False
    assert lamp.time_turned_off.strftime('%H:%M:%S') == datetime.now().strftime('%H:%M:%S')

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

def test_lamp_evaluate_need_below():
    """Tests the Lamp's evaluate_need method
    when it should be turned on"""
    lamp = Lamp(critical_value=10)
    lamp.evaluate_need(5)
    assert lamp.is_on is True

def test_lamp_evaluate_need_above():
    """Tests the Lamp's evaluate_need method
    when it should be turned off"""
    lamp = Lamp(critical_value=10)
    lamp.evaluate_need(15)
    assert lamp.is_on is False

def test_pump_evaluate_need_below():
    """Tests the Pump's evaluate_need method
    when it should be turned off"""
    pump = Pump(critical_value=10)
    pump.evaluate_need(5)
    assert pump.is_on is False

def test_pump_evaluate_need_above():
    """Tests the Pump's evaluate_need method
    when it should be turned off"""
    pump = Pump(critical_value=10)
    pump.evaluate_need(15)
    assert pump.is_on is True

def test_calc_time_on_same_interval():
    """Tests the Lamp's calculate_time_on method
    when turned on in the current interval"""
    now = datetime(2022,4,11,9,29,56)
    five_mins_ago = now - timedelta(minutes=5)
    five_mins_seconds = 5 * 60
    lamp = Lamp(is_on=True, time_turned_on=five_mins_ago)
    assert lamp.calculate_time_on(now) == five_mins_seconds

def test_calc_time_on_diff_interval():
    """Tests the Lamp's calculate_time_on method
    when turned on in a previous interval"""
    now = datetime(2022,4,11,9,29,56)
    twenty_mins_ago = now - timedelta(minutes=20)
    interval_seconds = 15 * 60
    lamp = Lamp(is_on=True, time_turned_on=twenty_mins_ago)
    assert lamp.calculate_time_on(now) == interval_seconds

def test_calc_time_off_same_interval():
    """Tests the Lamp's calculate_time_on method
    when off but turned on the same interval"""
    now = datetime(2022,4,11,9,29,56)
    seven_mins_ago = now - timedelta(minutes=7)
    five_mins_ago = now - timedelta(minutes=5)
    two_mins_seconds = 2 * 60
    lamp = Lamp(is_on=False, time_turned_on=seven_mins_ago,
        time_turned_off=five_mins_ago)
    assert lamp.calculate_time_on(now) == two_mins_seconds

def test_calc_time_off_diff_interval():
    """Tests the Lamp's calculate_time_on method
    when off but turned on in previous interval"""
    now = datetime(2022,4,11,9,29,56)
    twenty_mins_ago = now - timedelta(minutes=20)
    five_mins_ago = now - timedelta(minutes=5)
    nine_mins_seconds = 9 * 60
    lamp = Lamp(is_on=False, time_turned_on=twenty_mins_ago,
        time_turned_off=five_mins_ago)
    assert lamp.calculate_time_on(now) == nine_mins_seconds

def test_calc_time_twice_same_interval():
    """Tests the Lamp's calculate_time_on method
    when turned on & off twice in the same interval"""
    pass

def test_data_class_init():
    """Tests the Data class's DataArray post_init
    and getAvg methods"""
    moisture = 400
    light = 100
    data = Data(
        moisture_critical_value=moisture,
        light_critical_value=light)
    assert data.moistureArray.getAvg() == moisture
    assert data.lightArray.getAvg() == light

def test_data_class_array_updates():
    """Tests the Data class's DataArray update methods"""
    moisture = 400
    light = 100
    data = Data(
        moisture_critical_value=moisture,
        light_critical_value=light)
    # Yes, these are intentionally swapped
    # for a more noticeable difference
    data.moistureArray.add(light)
    data.lightArray.add(moisture)
    logging.debug(" Updated moistureArray: %s",
        data.moistureArray.data)
    logging.debug(" Updated lightArray: %s",
        data.lightArray.data)
    assert data.moistureArray.getAvg() == 340
    assert data.lightArray.getAvg() == 115
