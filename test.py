from dbiot import Dbiot
db = Dbiot(quiet=False)
# print(db.getApplicationFields(1))
# print(db.getSeriesMeasurements(1,0,0,20,2,"avg_celsius"))
print(db.getRawMeasurements(1,0,0,20,2))
db=None