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
select to_timestamp(groupumt) as umtdate,* from (
SELECT date_part('epoch',date_bin('15 minutes',to_timestamp(UMT),TIMESTAMP '2001-01-01')) as groupumt ,
 MAX(device_id) as device_id,MAX(application_id) as application_id,
AVG(hPa) as avg_hPa,MAX(hPa) as max_hPa,MIN(hPa) as min_hPa,
AVG(celsius) as avg_celsius,MAX(celsius) as max_celsius,MIN(celsius) as min_celsius,
AVG(humidity) as avg_humidity,MAX(humidity) as max_humidity,MIN(humidity) as min_humidity,
count(umt) FROM (select measurement.id,umt,
CAST(data->'hPa'  as DOUBLE PRECISION) as hPa,
CAST(data->'celsius'  as DOUBLE PRECISION) as celsius,
CAST(data->'humidity'  as DOUBLE PRECISION) as humidity,
device_id,application_id from measurement
WHERE application_id = 1
AND umt>=0
ORDER BY umt desc) as foo GROUP BY groupumt,device_id  ORDER BY groupumt
LIMIT 10) as fo2

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