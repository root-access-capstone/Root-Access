# Third Party
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


DATABASE_NAME = "root_access"
DATABASE_USER = "root"
DATABASE_PASS = "agroponics"

Base = declarative_base()

class Environments(Base):
    __tablename__ = "environments"
    envId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    data = sqlalchemy.orm.relationship("SensorData")
    plant = sqlalchemy.Column(sqlalchemy.String(length=40))
    minMoist = sqlalchemy.Column(sqlalchemy.Integer)

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    envId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('environments.envId'))
    whenCollected = sqlalchemy.Column(sqlalchemy.DateTime)
    timeLightOnMins = sqlalchemy.Column(sqlalchemy.Integer)
    waterConsumption = sqlalchemy.Column(sqlalchemy.Integer)
    powerConsumptionKwh = sqlalchemy.Column(sqlalchemy.Float)
    humidity = sqlalchemy.Column(sqlalchemy.Integer)
    soilMoisture = sqlalchemy.Column(sqlalchemy.Integer)
    temperature = sqlalchemy.Column(sqlalchemy.Integer)

class DailyMetrics(Base):
    __tablename__ = "daily_metrics"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    envId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('environments.envId'))
    dateProduced = sqlalchemy.Column(sqlalchemy.Date)
    totalWaterConsumption = sqlalchemy.Column(sqlalchemy.Integer)
    totalTimeLightOnMins = sqlalchemy.Column(sqlalchemy.Integer)
    totalPowerConsumptionKwh = sqlalchemy.Column(sqlalchemy.Float)

class EmailPass(Base):
    __tablename__ = "email_pass"
    email = sqlalchemy.Column(sqlalchemy.String(length=340), primary_key=True)
    password = sqlalchemy.Column(sqlalchemy.String(length=40))

class Database():
    def __init__(self):
        self.name = DATABASE_NAME
        self.user = DATABASE_USER
        self.password = DATABASE_PASS
        self.engine = self.createEngine()
        self.Session = self.createSession()
        self.createMetadata()
        self.initializeEnvironments()

    def createEngine(self) -> sqlalchemy.engine:
        """Returns sqlalchemy engine for the database"""
        engine = None
        try:
            engine = sqlalchemy.create_engine(f'mariadb+mariadbconnector://{self.user}:{self.password}@localhost:3306/{self.name}', echo = False)
        except Exception as error:
            print('**Error creating sqlalchemy engine: ', error)
        return engine

    def createSession(self) -> sqlalchemy.orm.Session:
        """Returns sqlalchemy Session for the database"""
        Session = None
        try:
            Session = sqlalchemy.orm.sessionmaker()
            Session.configure(bind=self.engine)
            Session = Session()
        except Exception as error:
            print('**Error creating database Session: ', error)
        return Session

    def createMetadata(self) -> None:
        """Creates tables if not exists"""
        try:
            Base.metadata.create_all(self.engine)
        except Exception as error:
            print('**Error creating database metadata: ', error)

    def initializeEnvironments(self) -> None:
        """Makes sure that there's an entry in the environments table for
        the sensor_data FK"""
        try:
            result = self.Session.query(Environments).filter(Environments.envId==1).first() is not None
            if not result:
                env = Environments(
                    envId = 1
                )
                self.Session.add(env)
                self.Session.commit()
                print('Created initial entry in environments table.')
        except Exception as error:
            print('**Error initializing environments: ', error)

def new_data_object(data:str) -> SensorData:
    """Returns new SensorData object from data string"""
    dataObject = None
    try:
        data = data.strip().split(',')
        if len(data) != 8:
            print('Error in new_data_object: Insufficient data to store in the database')
            return 0
        dataObject = SensorData(
            envId = data[0],
            whenCollected = data[1],
            timeLightOnMins = data[2],
            waterConsumption = data[3],
            powerConsumptionKwh = data[4],
            humidity = data[5],
            soilMoisture = data[6],
            temperature = data[7],
            )
    except Exception as error:
        print('**Error creating new SensorData object: ', error)
    return dataObject
