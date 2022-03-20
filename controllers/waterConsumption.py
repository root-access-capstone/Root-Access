def measureWaterConsumption(timePumpOn) -> int:
    """Takes the time the pump has been on (not sure the unit)
    times the flowrate & converts to seconds"""
    return timePumpOn * (100000 / 3600)
