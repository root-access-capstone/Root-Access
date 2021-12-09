class LightArray():
    """Array class for tracking average of light values"""
    def __init__(self, length:int) -> None:
        self.data = [0] * length

    def add(self, x:str):
        self.data.append(int(x))
        self.data.pop(0)

    def getAvg(self):
        return sum(self.data)/len(self.data)
