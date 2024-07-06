from dbiot import Dbiot

db = Dbiot(quiet=False)
table = db.listTable("SELECT * FROM test")
for row in table:
    print(row[0])
db = None