import logging
from dataclasses import dataclass, field
from controllers.dataArray import DataArray


@dataclass
class Data:
    """Dataclass for passing sensor data around"""
    temperature:int = 0
    humidity:int = 0
    moisture:int = 0
    moistureArray:DataArray = field(init=False)
    lightArray:DataArray = field(init=False)
    moisture_critical_value:int = 400
    light_critical_value:int = 100
    valid:bool = False

    def __post_init__(self):
        """Initializes DataArrays for moisture & light
        with their proper critical values"""
        moist_length = 5
        light_length = 20
        self.moistureArray:DataArray = DataArray(
            self.moisture_critical_value,
            moist_length)
        logging.debug(" Initialized moistureArray: \n\t%s",
            self.moistureArray.data)
        self.lightArray:DataArray = DataArray(
            self.light_critical_value,
            light_length)
        logging.debug(" Initialized lightArray: \n\t%s",
            self.lightArray.data)

    def update(self, temperature:int, humidity:int,
            moisture:int, light:int) -> bool:
        """Updates temperature, humidity, and moisture,
        checks their validity, and adds moisture &
        light to their DataArrays"""
        invalid_data = [0, -999]
        if temperature in invalid_data or moisture in invalid_data:
            logging.debug(" Invalid data received: %s",
                [temperature, humidity, moisture, light])
            self.valid = False
            return self.valid
        logging.debug(" Updating Data: %s",
            [temperature, humidity, moisture, light])
        self.valid = True
        self.temperature = temperature
        self.humidity = humidity
        self.moisture = moisture
        self.moistureArray.add(moisture)
        self.lightArray.add(light)
        return self.valid
