from datetime import datetime
import time
from dbiot import Dbiot
db = Dbiot(quiet=False)
# print(db.getApplicationFields(1))
# print(db.getSeriesMeasurements(1,0,0,20,2,"avg_celsius"))
# print(db.getRawMeasurements(1,0,0,20,2))
print(db.getApplicationDevice(1,3))
db=None
# dte =datetime.fromisoformat("1970-01-01T00:00:00")
# dt =datetime.fromisoformat("2024-07-31T09:57:05.324105")
# utcHologram = time.mktime(dt.timetuple()) - time.mktime(dte.timetuple())
# print(utcHologram)




