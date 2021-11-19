import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

DATABASE_NAME = "root_access"
DATABASE_TABLES = ["environments", "sensor_data", "daily_metrics"]
DATABASE_USER = "root"
DATABASE_PASS = "agroponics"

def create_database_handler():
    engine = create_engine(f'mysql+mysqldb://{DATABASE_USER}:{DATABASE_PASS}@localhost/{DATABASE_NAME}', echo = False)
    return engine

def ensure_environments_table(handler):
    query = 'SELECT * FROM environments'
    result = handler.execute(query).fetchall()
    if len(result) == 0:
        handler.execute('INSERT INTO environments (envId) VALUES (0)')
        print('Created initial environments row.')
    else:
        print('Table environments is already initialized.')

def send_data(data:str):
    handler = create_database_handler()
    ensure_environments_table()
    columns = ['envId', 'whenCollected', 'timeLightOnMins', 'humidity',
        'soilMoisture', 'temperature', 'waterConsumption']
    data = data.strip().split(',')
    df = pd.DataFrame(data = data, columns = columns)
    try:
        df.to_sql('sensor_data', handler)
    except ValueError:
        print('Table already exists, might be an issue with if_exists.')
    sd = handler.execute('SELECT * FROM sensor_data').fetchall()
    print(sd)

if __name__ == '__main__':
    send_data()