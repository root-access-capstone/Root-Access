class LightArray():
    """Array class for tracking average of light values"""
    def __init__(self) -> None:
        self.data = [0] * 30

    def add(self, x:int):
        assert type(x)=='int', 'Wrong datatype for light array'
        self.data.append(x)
        self.data.pop()

    def getAvg(self):
        return sum(self.data)/len(self.data)