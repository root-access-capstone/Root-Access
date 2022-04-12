import logging

from controllers.powerConsumption import measurePowerConsumption
from controllers.waterConsumption import measureWaterConsumption


logging.basicConfig(level=logging.DEBUG)

def test_lamp_power():
    """Tests measurePowerConsumption with lamp time
    set to 1 hour"""
    result = measurePowerConsumption(lampSeconds=3600)
    assert round(result, 3) == 0.015

def test_pump_power():
    """Tests measurePowerConsumption with pump time
    set to 1 hour"""
    result = measurePowerConsumption(pumpSeconds=3600)
    assert round(result, 3) == 0.013

def test_water_consumption():
    """Tests measureWaterConsumption with pump time
    set to 1 hour"""
    result = measureWaterConsumption(pumpOnTimeSecs=3600)
    assert result == 100000
