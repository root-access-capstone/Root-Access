def measureWaterConsumption(timePumpOn) -> int:
    """
	Takes the time the pump has been on in seconds
	times the flowrate in seconds
	"""
    return timePumpOn * (100000 / 3600)
