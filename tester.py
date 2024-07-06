from dbiot import Dbiot

db = Dbiot(quiet=False)
print(db.addMeasurement(1,1,1,{"temprature":24}))
db = None