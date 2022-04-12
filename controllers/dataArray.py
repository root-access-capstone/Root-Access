from statistics import mean

class DataArray():
    """Array class for tracking average of data values"""
    def __init__(self, critical_value:int, length:int) -> None:
        self.data = [critical_value] * length

    def add(self, value:int) -> None:
        """Adds the new value and removes the oldest"""
        self.data.append(value)
        self.data.pop(0)

    def getAvg(self) -> float:
        """Just uses the statistics mean function"""
        return mean(self.data)
