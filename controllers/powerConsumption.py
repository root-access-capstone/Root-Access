def wattsToKWH(x:int) -> int:
    """Convert watts to kilowatt hours"""
    return x/3600000

def measurePowerConsumption(pumpMinutes:int=0, lampMinutes:int=0) -> int:
    """Measures power consumption in KWH"""
    watt_usage_ref = { # Measured in Watts
        'lamp': 14,
        'pump': 1.85,
        'system': 4
    }

    powerConsumption = 0
    try:
        for k, v in watt_usage_ref.items():
            if k == 'lamp' and lampMinutes:
                powerConsumption += (v * (lampMinutes*60))
            elif k == 'pump' and pumpMinutes:
                powerConsumption += (v * (pumpMinutes*60))
            elif k != 'lamp' and k != 'pump':
                powerConsumption += (v * (900))
    except Exception as error:
        print('**Error computing powerConsumption: ', error)

    powerConsumptionKWH = wattsToKWH(powerConsumption)
    return powerConsumptionKWH

if __name__ == '__main__':
    pc = measurePowerConsumption(lampMinutes=7)
    assert round(pc, 6) == 0.005267, 'Incorrect power consumption output: '+str(round(pc, 6))
    print(round(pc, 6), 'kwh')
