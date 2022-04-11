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

def compare_old_calc_to_new():
    """Compares old calculate_time_on
    function with the new one"""
    now = datetime(2022,4,11,9,29,56)
    print('='*60)
    print("Assuming that the current time is "
        f"{now.strftime('%H:%M:%S')}, here are "
        "the various comparisons (old = new):")
    five_mins_ago = now - timedelta(minutes=5)
    seven_mins_ago = now - timedelta(minutes=7)
    twenty_mins_ago = now - timedelta(minutes=20)
    peripheral = Peripheral(is_on=True, time_turned_on=five_mins_ago)
    print('-'*60)
    print("\n\tOn same interval - ",
        f"{peripheral.calculate_time_on(now)} =",
        f"{peripheral.new_calc(now)}")

    peripheral.time_turned_on = twenty_mins_ago
    print('-'*60)
    print("\n\tOn different interval - ",
        f"{peripheral.calculate_time_on(now)} =",
        f"{peripheral.new_calc(now)}")

    peripheral.is_on = False
    peripheral.time_turned_on = seven_mins_ago
    peripheral.time_turned_off = five_mins_ago
    print('-'*60)
    print("\n\tOff same interval - ",
        f"{peripheral.calculate_time_on(now)} =",
        f"{peripheral.new_calc(now)}")

    peripheral.time_turned_on = twenty_mins_ago
    peripheral.time_turned_off = five_mins_ago
    print('-'*60)
    print("\n\tOff different interval - ",
        f"{peripheral.calculate_time_on(now)} =",
        f"{peripheral.new_calc(now)}") # 10 mins

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

# test_calc_time_on_same_interval()
# test_calc_time_on_diff_interval()
# test_calc_time_off_same_interval()
# test_calc_time_off_diff_interval()
compare_old_calc_to_new()
