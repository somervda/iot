from dbiot import Dbiot
import json
import urllib.request
import time
from datetime import datetime
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
            print("Loading data:",time.time(),contents)
            data = json.loads(contents)
            application_id = data["appID"]
            del data["appID"]
            device_id = data["deviceID"]
            del data["deviceID"]
            # Set umt time to best available time when event occured
            if "sensorTimestamp" in data:
                # sensorTimestamp is time event occured on the sensor
                umt = data["sensorTimestamp"]
            elif "iotTimestamp" in data:
                # iotTimestamp is when the measurement was sent to the IOT cache
                umt = data["iotTimestamp"]
            elif "received" in data:
                # recieved is the best timestamp seen in hologram.io data if no other timestamps set
                # Little bit of hacky code to adjust recieve to be interpreted as utc iso date 
                rumt = time.time( data["iotTimestamp"])
                dte =datetime.fromisoformat("1970-01-01T00:00:00")
                dt =datetime.fromisoformat("2024-07-31T09:57:05.324105")
                utcHologram = time.mktime(dt.timetuple()) - time.mktime(dte.timetuple())
                umt = utcHologram
            else:
                umt = time.time()
            if "sensorTimestamp" in data:
                del data["sensorTimestamp"]
            if "iotTimestamp" in data:
                del data["iotTimestamp"]
            if "received" in data:
                del data["received"]
            print(data)

            db = Dbiot(quiet=False)
            print(db.addMeasurement(umt,application_id,device_id,data,adjustEpoch=False))
            db = None
            time.sleep(.1)
    except Exception as error:
        print("An exception occurred:", error)
        time.sleep(10)