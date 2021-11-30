# Third Party
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


DATABASE_NAME = "root_access"
DATABASE_USER = "root"
DATABASE_PASS = "agroponics"

Base = declarative_base()

class Data(Base):
    __tablename__ = "sensor_data"
    envId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    whenCollected = sqlalchemy.Column(sqlalchemy.DateTime)
    timeLightOnMins = sqlalchemy.Column(sqlalchemy.Integer)
    humidity = sqlalchemy.Column(sqlalchemy.Integer)
    soilMoisture = sqlalchemy.Column(sqlalchemy.Integer)
    temperature = sqlalchemy.Column(sqlalchemy.Integer)
    waterConsumption = sqlalchemy.Column(sqlalchemy.Integer)

def create_database_handler():
    engine = sqlalchemy.create_engine(f'mariadb+mariadbconnector://{DATABASE_USER}:{DATABASE_PASS}@localhost:3306/{DATABASE_NAME}', echo = False)
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
    data = data.strip().split(',')
    if len(data) != 7:
        print('**Error in send_data: Insufficient data to store in the database.')
    else:
        handler = create_database_handler()
        # ensure_environments_table()
        try:
            Base.metadata.create_all(handler)
        except Exception as error:
            print('**Error creating Base metadata: ', error)
        try:
            Session = sqlalchemy.orm.sessionmaker()
            Session.configure(bind = handler)
            Session = Session()
        except Exception as error:
            print('**Error creating database Session: ', error)
        try:
            newData = Data(
                envId = data[0],
                whenCollected = data[1],
                timeLightOnMins = data[2],
                humidity = data[3],
                soilMoisture = data[4],
                temperature = data[5],
                waterConsumption = data[6]
            )
        except Exception as error:
            print('**Error creating new Data object: ', error)
        try:
            Session.add(newData)
            Session.commit()
            result = Session.query(Data).all()
            print(result)
        except Exception as error:
            print('**Error adding to or querying database: ', error)

if __name__ == '__main__':
    incoming = '0,2021-04-22 02:22:22,2,4,100,10,3'
    send_data(incoming)