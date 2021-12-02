# Third Party
from datetime import datetime, timedelta

def wattsToKWH(x:int) -> int:
    """Convert watts to kilowatt hours"""
    return x/3600000

def measurePowerConsumption(pumpStartTime:datetime=None, lampStartTime:datetime=None) -> int:
    """Measures power consumption in KWH"""
    watt_usage_ref = { # Measured in Watts
        'lamp': 13, # Actual
        'pump': 0.85, # Actual
        'rasp-pi': 10, # TBD
        'arduino': 5 # TBD
    }

    endTime = datetime.now()
    powerConsumption = 0
    try:
        for k, v in watt_usage_ref.items():
            if k == 'lamp' and lampStartTime:
                powerConsumption += (v * ((endTime-lampStartTime).seconds))
            elif k == 'pump' and pumpStartTime:
                powerConsumption += (v * ((endTime-pumpStartTime).seconds))
            elif k != 'lamp' and k != 'pump':
                powerConsumption += (v * (900))
    except Exception as error:
        print('**Error computing powerConsumption: ', error)

    powerConsumptionKWH = wattsToKWH(powerConsumption)
    return powerConsumptionKWH

if __name__ == '__main__':
    time = datetime.now() - timedelta(minutes=7)
    pc = measurePowerConsumption(lampStartTime=time)
    assert round(pc, 6) == 0.005266, 'Incorrect power consumption output.'
    print(pc, 'kwh')
