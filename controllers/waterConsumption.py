def measureWaterConsumption(pumpOnTimeSecs:int) -> int:
    """
    Takes the time the pump has been on in seconds
    times the flowrate in seconds
    """
    flowrate = 100000
    return pumpOnTimeSecs * (flowrate / 3600)
