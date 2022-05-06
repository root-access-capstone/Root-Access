import pandas as pd
from datetime import datetime


from controllers.database import Database, SensorData


def main():
    today = datetime.now().today()
    db = Database()
    result = db.Session.query(SensorData).all()
    df = pd.DataFrame(result)
    df.to_csv(f"root_access_export_{today}.csv")

if __name__ == '__main__':
    main()
