from dbiot import Dbiot
import json
import urllib.request
import time
# Useful select to see recent data
# select measurement.id,umt,to_timestamp(umt) as umtdate,data,
# ((data->>'celsius')::numeric * 9/5) + 32 as fahrenheit,
# application_id,device_id,application.name,device.name from measurement 
# JOIN application ON measurement.application_id = application.id
# JOIN device ON measurement.device_id = device.id
# order by umt desc
# limit 10

while True:
    try:
        contents = urllib.request.urlopen("http://somerville.noip.me:37007/read?user=david").read()
        if contents.decode('ascii')=='None':
            print("end of data - sleeping 3 minutes...")
            time.sleep(180)
        else:
            data = json.loads(contents)
            application_id = data["appID"]
            del data["appID"]
            device_id = data["deviceID"]
            del data["deviceID"]
            umt = data["sensorTimestamp"]
            del data["sensorTimestamp"]
            del data["iotTimestamp"]

            print(data)

            db = Dbiot(quiet=False)
            print(db.addMeasurement(umt,application_id,device_id,data,adjustEpoch=False))

            # print(Dbiot.listTable("select cast(to_timestamp(umt) as date) as umtdate from measurement"))
            db = None
            time.sleep(1)
    except Exception as error:
        print("An exception occurred:", error)
        time.sleep(10)