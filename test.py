from dbiot import Dbiot
db = Dbiot(quiet=False)
# print(db.getApplicationMeasurements(1))
print(db.getMeasurements(1,0,0,20,2))
db=None