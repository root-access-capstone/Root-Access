from classes import Peripheral
from datetime import datetime, timedelta
import logging

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

def test_evaluate_need():
    """Tests the Peripheral's evaluate_need method"""
    peripheral = Peripheral(critical_value=10)
    peripheral.evaluate_need(15)
    assert peripheral.is_on is False
    peripheral.evaluate_need(5)
    assert peripheral.is_on is True

def test_time_on():
    """Tests the Peripheral's calculate_time_on method"""
    five_mins_ago = datetime.now() - timedelta(minutes=5)
    five_mins_seconds = 60 * 5
    peripheral = Peripheral(is_on=True, time_turned_on=five_mins_ago)
    print(peripheral.time_turned_on.minute % 15, datetime.now().minute % 15)
    assert peripheral.calculate_time_on() == five_mins_seconds
    twenty_mins_ago = datetime.now() - timedelta(minutes=21)
    fifteen_mins_seconds = 60 * 15
    peripheral.time_turned_on = twenty_mins_ago
    print(peripheral)
    print(peripheral.calculate_time_on())
    # assert peripheral.calculate_time_on() == fifteen_mins_seconds
    # need to subtract now from the last 15 min interval
    # currently just subtracts 15 mins from the difference in seconds
    # which is obviously not right.
    print(peripheral.time_turned_on.minute % 15, datetime.now().minute % 15)

def test_calc_time_on_same_interval():
    """Tests the Peripheral's calculate_time_on method
    when turned on in the current interval"""
    now = datetime(2022,4,11,9,29,56)
    five_mins_ago = now - timedelta(minutes=5)
    five_mins_seconds = 5 * 60
    peripheral = Peripheral(is_on=True, time_turned_on=five_mins_ago)
    assert peripheral.new_calc(now) == five_mins_seconds

def test_calc_time_on_diff_interval():
    """Tests the Peripheral's calculate_time_on method
    when turned on in a previous interval"""
    now = datetime(2022,4,11,9,29,56)
    twenty_mins_ago = now - timedelta(minutes=20)
    interval_seconds = 15 * 60
    peripheral = Peripheral(is_on=True, time_turned_on=twenty_mins_ago)
    assert peripheral.new_calc(now) == interval_seconds

def test_calc_time_off_same_interval():
    """Tests the Peripheral's calculate_time_on method
    when off but turned on the same interval"""
    now = datetime(2022,4,11,9,29,56)
    seven_mins_ago = now - timedelta(minutes=7)
    five_mins_ago = now - timedelta(minutes=5)
    two_mins_seconds = 2 * 60
    peripheral = Peripheral(is_on=False, time_turned_on=seven_mins_ago,
        time_turned_off=five_mins_ago)
    print("calc",peripheral.new_calc(now))
    assert peripheral.new_calc(now) == two_mins_seconds

def test_calc_time_off_diff_interval():
    """Tests the Peripheral's calculate_time_on method
    when off but turned on in previous interval"""
    now = datetime(2022,4,11,9,29,56)
    twenty_mins_ago = now - timedelta(minutes=20)
    five_mins_ago = now - timedelta(minutes=5)
    nine_mins_seconds = 9 * 60
    peripheral = Peripheral(is_on=False, time_turned_on=twenty_mins_ago,
        time_turned_off=five_mins_ago)
    assert peripheral.new_calc(now) == nine_mins_seconds

def test_new():
    now = datetime(2022,4,11,9,31,56)
    five_mins_ago = now - timedelta(minutes=5)
    three_mins_ago = now - timedelta(minutes=3)
    peripheral = Peripheral(is_on=True, time_turned_on=five_mins_ago, time_turned_off=three_mins_ago)
    print(peripheral)
    print("div", peripheral.time_turned_on.minute // 15, now.minute // 15)
    print("mod", peripheral.time_turned_on.minute % 15, now.minute % 15)
    # print(peripheral.time_turned_on.minute, now.minute)
    # print(now-peripheral.time_turned_on)
    print("calc", peripheral.new_calc(now))
    # print("calc", peripheral.calculate_time_on(now))

    # assert peripheral.new_calc() == five_mins_seconds

    # cases: (written late at night, double check)
    # 1) on in the same 15 min interval ( both // 15)
    #   time = now - time_turned_on
    #
    # 2) different 15 min interval, still on ( both % 15)
    #   time = now % 15 mins
    #
    # 3) off same interval ( both // 15)
    #   time = time_turned_off - time_turned_on
    #
    # 4) off different interval ( both % 15)
    #   time = time_turned_off % 15 mins
    #
    # what about when the minute is 15 but it turned on that interval...?

# test_new()

# test_calc_time_on_same_interval()
# test_calc_time_on_diff_interval()
test_calc_time_off_same_interval()
# test_calc_time_off_diff_interval()
