from dbiot import Dbiot
db = Dbiot(quiet=False)
# print(db.getApplicationMeasurements(1))
print(db.getSeriesMeasurements(1,0,0,20,2,"avg_celsius"))
db=None