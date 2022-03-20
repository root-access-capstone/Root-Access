from statistics import mean

class DataArray():
    """Array class for tracking average of data values"""
    def __init__(self, inflectionPoint:int, length:int) -> None:
        self.data = [inflectionPoint] * length

    def add(self, x:str):
        self.data.append(int(x))
        self.data.pop(0)

    def getAvg(self):
        return mean(self.data)
