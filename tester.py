from dbiot import Dbiot

db = Dbiot(quiet=False)
# table = db.listTable("SELECT * FROM test")
# for row in table:
#     print(row['num'])
print(db.addMeasurement(1,1,1,'{"temprature":24}'))
db = None