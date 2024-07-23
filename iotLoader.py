from dbiot import Dbiot
import json
import urllib.request
import time
""" 
Useful SQL to see recent data

select measurement.id,umt,to_timestamp(umt) as umtdate,data,
((data->>'celsius')::numeric * 9/5) + 32 as fahrenheit,
device_id,application_id,application.name,device.name from measurement 
JOIN application ON measurement.application_id = application.id
JOIN device ON measurement.device_id = device.id
order by umt desc
limit 10

Example: Group into daily trends
SELECT to_timestamp(date_part('epoch',date_trunc('day',to_timestamp(UMT)))) as date
,MAX(device_id) as device_id,MAX(application_id) as application_id,
AVG(fahrenheit) as avg_fahrenheit,
count(umt) FROM (
select measurement.id,umt,to_timestamp(umt) as umtdate,data,
((data->>'celsius')::numeric * 9/5) + 32 as fahrenheit,
device_id,application_id,application.name,device.name from measurement 
JOIN application ON measurement.application_id = application.id
JOIN device ON measurement.device_id = device.id
) as foo 
GROUP BY date,device_id 
ORDER BY date desc

"""

while True:
    try:
        contents = urllib.request.urlopen("http://somerville.noip.me:37007/read?user=david").read()
        if contents.decode('ascii')=='None':
            print("End of iotCache data - sleeping 30 seconds...")
            time.sleep(30)
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
            db = None
            time.sleep(.1)
    except Exception as error:
        print("An exception occurred:", error)
        time.sleep(10)