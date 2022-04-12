import logging


def wattsToKWH(x:int) -> int:
    """Convert watts to kilowatt hours"""
    seconds_per_hour = 3600
    return (x/seconds_per_hour)/1000

def measurePowerConsumption(pumpSeconds:int=0, lampSeconds:int=0) -> int:
    """Measures power consumption in KWH"""
    watt_usage_ref = { # Measured in Watts
        'lamp': 14,
        'pump': 12,
        'system': 4
    }

    powerConsumption = 0
    try:
        for k, v in watt_usage_ref.items():
            logging.debug(" %s: %s", k, v)
            if k == 'lamp' and lampSeconds:
                powerConsumption += (v * (lampSeconds))
            elif k == 'pump' and pumpSeconds:
                powerConsumption += (v * (pumpSeconds))
            elif k != 'lamp' and k != 'pump':
                powerConsumption += (v * (900))
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
