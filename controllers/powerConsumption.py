import logging


def wattsToKWH(value:int) -> int:
    """Convert watts to kilowatt hours"""
    seconds_per_hour = 3600
    return (value/seconds_per_hour)/1000

def measurePowerConsumption(pumpSeconds:int=0, lampSeconds:int=0) -> int:
    """Measures power consumption in KWH"""
    watt_usage_ref = { # Measured in Watts
        'lamp': 14,
        'pump': 12,
        'system': 4
    }

    powerConsumption = 0
    try:
        for key, watts in watt_usage_ref.items():
            logging.debug(" %s: %s", key, watts)
            if key == 'lamp' and lampSeconds:
                powerConsumption += (watts * (lampSeconds))
            elif key == 'pump' and pumpSeconds:
                powerConsumption += (watts * (pumpSeconds))
            elif key != 'lamp' and key != 'pump':
                powerConsumption += (watts * (900))
            logging.debug(" End of loop power consumption = %s",
                powerConsumption)
    except Exception as error:
        logging.error(' Error computing powerConsumption: %s',
            error)

    powerConsumptionKWH = wattsToKWH(powerConsumption)
    return powerConsumptionKWH

if __name__ == '__main__':
    pc = measurePowerConsumption(lampSeconds=60)
    assert round(pc, 6) == 0.005267, 'Incorrect power consumption output: '+str(round(pc, 6))
    print(round(pc, 6), 'kwh')
