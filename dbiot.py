#!/usr/bin/python3

import psycopg
from psycopg.rows import dict_row
import json

class Dbiot:

    _quiet = True
    _conn = None
    _cur = None

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self._conn = psycopg.connect("dbname=iotdb user=pi")
        self._cur = self._conn.cursor(row_factory=dict_row)

    def listTable(self,sql):
        not self._quiet and print("listTable",sql)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def getApplicationFields(self,application_id):
        not self._quiet and print("getApplicationFields:",application_id)
        sql = "SELECT fields FROM application WHERE id=" + str(application_id)
        self._cur.execute(sql)
        return self._cur.fetchone()["fields"]

# Device

    def deviceExists(self,device_id):
        not self._quiet and print("deviceExist",device_id)
        sql = "select count(*) as count from device where id=" + str(device_id)
        self._cur.execute(sql)
        result = self._cur.fetchone()["count"]
        if result == 1:
            return True
        else:
            return False

    def addDevice(self,name,description):
        not self._quiet and print("addDevice",name,description)
        sql = ("INSERT INTO device (name,description) VALUES ('%s', '%s')" %
            (name,description))
        not self._quiet and print("addDevice sql:",sql)
        result = self._cur.execute(sql)
        self._conn.commit()

    def deleteDevice(self,id):
        not self._quiet and print("deleteDevice",id)
        sql = "delete from device where id=" + str(id)
        not self._quiet and print("deleteDevice sql:",sql)
        result = self._cur.execute(sql)
        self._conn.commit()

    def updateDevice(self,id,name,description):
        not self._quiet and print("updateDevice",id,name,description)
        sql = ("update device set name='%s', description='%s' where id=%s"  %
            (name,description,id))
        not self._quiet and print("updateDevice sql:",sql)
        result = self._cur.execute(sql)
        self._conn.commit()

#  Application
    def applicationExists(self,application_id):
        not self._quiet and print("applicationExist",application_id)
        sql = "select count(*) as count from application where id=" + str(application_id)
        self._cur.execute(sql)
        result = self._cur.fetchone()["count"]
        if result == 1:
            return True
        else:
            return False

    def addApplication(self,name,description,fields):
        # example db.addApplication("t","xxx",['a','b'])
        not self._quiet and print("addApplication",name,description,fields)
        sql = ("INSERT INTO application (name,description,fields) VALUES ('%s', '%s',ARRAY %s)" %
            (name,description,fields))
        not self._quiet and print("addApplication sql:",sql)
        result = self._cur.execute(sql)
        self._conn.commit()

    def deleteApplication(self,id):
        not self._quiet and print("deleteApplication",id)
        sql = "delete from application where id=" + str(id)
        not self._quiet and print("deleteApplication sql:",sql)
        result = self._cur.execute(sql)
        self._conn.commit()

    def updateApplication(self,id,name,description,fields):
        # Eg db.updateApplication(6,"update","new",['x','y','z'])
        not self._quiet and print("updateApplication",id,name,description,fields)
        sql = ("update application set name='%s', description='%s', fields=ARRAY %s where id=%s"  %
            (name,description,fields,id))
        not self._quiet and print("updateApplication sql:",sql)
        result = self._cur.execute(sql)
        self._conn.commit()

# ApplicationDevice
    def applicationDeviceExists(self,application_id,device_id):
        not self._quiet and print("applicationDeviceExists",application_id,device_id)
        sql = "select count(*) as count from applicationDevice where application_id=" + str(application_id) + " and device_id=" + str(device_id)
        self._cur.execute(sql)
        result = self._cur.fetchone()["count"]
        if result == 1:
            return True
        else:
            return False

    def getApplicationDevices(self,application_id):
        # Get the devices that support a particuler application
        not self._quiet and print("getApplicationDevices",application_id)
        sql = "select device.*" 
        sql += "\nfrom applicationDevice "
        sql += "\nJOIN device ON applicationDevice.device_id = device.id"
        sql += "\nwhere applicationDevice.application_id =" + str(application_id)
        return self.listTable(sql)

    def getDeviceApplications(self,device_id):
        # Get the devices that support a particuler application
        not self._quiet and print("getDeviceApplications",device_id)
        sql = "select application.*" 
        sql += "\nfrom applicationDevice "
        sql += "\nJOIN application ON applicationDevice.application_id = application.id"
        sql += "\nwhere applicationDevice.device_id =" + str(device_id)
        return self.listTable(sql)

    def getDeviceApplicationsStatus(self,device_id):
        # Get the applications for a particuler device
        # and the most reciend measurements
        not self._quiet and print("getDeviceApplicationsStatus",device_id)
        sql = "select applicationDevice.*,application.name,application.description" 
        sql += "\nfrom applicationDevice "
        sql += "\nJOIN application ON applicationDevice.application_id = application.id"
        sql += "\nwhere applicationDevice.device_id =" + str(device_id)
        return self.listTable(sql)

    def getApplicationDevice(self,application_id,device_id):
        # Get the devices that support a particuler application
        not self._quiet and print("getApplicationDevice",application_id)
        sql = "select *" 
        sql += "\nfrom applicationDevice "
        sql += "\nwhere applicationDevice.device_id =" + str(device_id)
        sql += "\nand applicationDevice.application_id =" + str(application_id)
        return self.listTable(sql)

# Measurement

    def addMeasurement(self, umt,application_id,device_id,data,adjustEpoch=False):
        not self._quiet and print("addMeasurement",umt,application_id,device_id,data,adjustEpoch)
        if adjustEpoch:
            # micropython frequently uses a epoch start of 1Jan2000, this flag
            # will change the value to a unix epoch
            umt += 946684800 
        # Check device is valid
        if not self.deviceExists(device_id):
            return("addMeasurement","Device does not exist",device_id)
        if not self.applicationExists(application_id):
            return("addMeasurement","Application does not exist",application_id)
        # Check to see if applicationDevice exist, eitherr update it or create one
        # applicationDevice is generally self populating, but can be set up first
        if self.applicationDeviceExists(application_id,device_id):
            sql = ("UPDATE applicationDevice set umt=%s, data='%s'::jsonb where application_id=%s and device_id=%s" %
                (umt,json.dumps(data),application_id,device_id))
            not self._quiet and print("addMeasurement appDev sql:",sql)
            self._cur.execute(sql)
        else:
            sql = ("INSERT INTO applicationDevice (umt,application_id,device_id,data) VALUES (%s, %s,%s,'%s')" %
                (umt,application_id,device_id,json.dumps(data)))
            not self._quiet and print("addMeasurement appDev sql:",sql)
            self._cur.execute(sql)
        # umt is Universal Metric Time in seconds since 1Jan1970 (UNIX epoch)
        sql = ("INSERT INTO measurement (umt,application_id,device_id,data) VALUES (%s, %s,%s,'%s')" %
            (umt,application_id,device_id,json.dumps(data)))
        not self._quiet and print("addMeasurement sql:",sql)
        result = self._cur.execute(sql)
        # Createor update a
        self._conn.commit()
        return result


    def getRawMeasurements(self,application_id,device_id,timestamp,rows,grouping):
        # grouping values 0=None, 1=5 minutes,2=15 minutes,3=hour,4=6 hours, 5=day,6=week,7=month,8=3 month,9=year
        not self._quiet and print("getRawMeasurements: app=",application_id," dev=",device_id," timestamp=",timestamp," rows=",rows, " grouping=",grouping)
        applicationFields=self.getApplicationFields(application_id)
        # get and return data
        sql = "select measurement.id,umt,"
        for field in applicationFields:
            sql += "\nCAST(data->'" + field + "'  as DOUBLE PRECISION) as " + field +","
        sql += "\ndevice_id,application_id from measurement"
        sql += "\nWHERE application_id = " + str(application_id) 
        sql += "\nAND umt>=" + str(timestamp)
        if device_id != 0:
            sql += "\nAND device_id=" + str(device_id) 
        sql += "\nORDER BY umt desc"
        groupingSQL = "SELECT date_part('epoch',"
        if grouping==1:
            groupingSQL += "date_bin('5 minutes',to_timestamp(UMT),TIMESTAMP '2001-01-01')"
        if grouping==2:
            groupingSQL += "date_bin('15 minutes',to_timestamp(UMT),TIMESTAMP '2001-01-01')"
        if grouping==3:
            groupingSQL += "date_bin('1 hour',to_timestamp(UMT),TIMESTAMP '2001-01-01')"
        if grouping==4:
            groupingSQL += "date_bin('6 hours',to_timestamp(UMT),TIMESTAMP '2001-01-01')"
        if grouping==5:
            groupingSQL += "date_trunc('day',to_timestamp(UMT))"
        if grouping==6:
            groupingSQL += "date_trunc('week',to_timestamp(UMT))"
        if grouping==7:
            groupingSQL += "date_trunc('month',to_timestamp(UMT))"
        if grouping==8:
            groupingSQL += "date_trunc('quarter',to_timestamp(UMT))"
        if grouping==9:
            groupingSQL += "date_trunc('year',to_timestamp(UMT))"
        groupingSQL += ") as groupumt ,\n MAX(device_id) as device_id,MAX(application_id) as application_id,"
        # groupingSQL += "\ndate as umt,"
        for field in applicationFields:
            groupingSQL += "\nAVG(" + field + ") as avg_" + field + ","
            groupingSQL += "MAX(" + field + ") as max_" + field + ","
            groupingSQL += "MIN(" + field + ") as min_" + field + ","
        groupingSQL += "\ncount(umt) FROM (" + sql + ") as foo GROUP BY groupumt,device_id "
        if device_id != 0:
            # also group by device id if more than one selected (device_id!=0)
            sql += ", device_id" 
        groupingSQL += " ORDER BY groupumt"
        # AVG(celsius),count(umt) FROM (" + sql + ") as foo GROUP BY date ORDER BY date" 
        if grouping==0:
            sql += "\nLIMIT " + str(rows)
            not self._quiet and print("sql:",sql)
            self._cur.execute(sql)
        else:
            groupingSQL += "\nLIMIT " + str(rows)
            not self._quiet and print("sql:",groupingSQL)
            self._cur.execute(groupingSQL)
        result = self._cur.fetchall()
        if grouping!=0:
            # Rename the groupumt dict item for grouped results
            for measurement in result:
                measurement["umt"] = measurement.pop("groupumt")
        return result

    def getFlatMeasurements(self,application_id,device_id,timestamp,rows,grouping,field):
        not self._quiet and print("getFlatMeasurements: app=",application_id," dev=",device_id," timestamp=",timestamp," rows=",rows, " grouping=",grouping," field=",field)
        # Just return specific requested field
        fullResult = self.getRawMeasurements(application_id,device_id,timestamp,rows,grouping)
        # Just return date and selected field
        result = []
        try:
            for measurement in fullResult:
                result.append({"umt":measurement["umt"],"0":measurement[field]})
        except Exception as error:
            not self._quiet and print("An exception occurred, field name error:", error)
            result=[]
        return result

    def getSeriesMeasurements(self,application_id,device_id,timestamp,rows,grouping,field):
        not self._quiet and print("getSeriesMeasurements: app=",application_id," dev=",device_id," timestamp=",timestamp," rows=",rows, " grouping=",grouping," field=",field)
        # Just return specific requested field
        fullResult = self.getRawMeasurements(application_id,device_id,timestamp,rows,grouping)
        # Just return date and selected field
        result = []
        try:
            for measurement in fullResult:
                result.append({"umt":measurement["umt"],str(measurement["device_id"]):measurement[field]})
        except Exception as error:
            not self._quiet and print("An exception occurred, field name error:", error)
            result=[]
        # change iotData into a series structure ["name":"0","series":[{"umt":nnn,"value":nnnn}]]
        resultSeries = []
        for measurement in result:
            umt = measurement["umt"]
            for keys in measurement.keys():
                if keys != "umt":
                    device_id = keys
                    value = measurement.get(keys,None)
            self.addToSeries(resultSeries,umt,device_id,value)
        return resultSeries

    def addToSeries(self,resultSeries,umt,device_id,value):
        deviceSeries = None
        for series in resultSeries:
            if series.get("name",-1) == int(device_id):
                # Series exists for the device
                deviceSeries=series
                break
        if deviceSeries==None:
            resultSeries.append({"name":int(device_id),"series": []})
            for series in resultSeries:
                if series.get("name",-1) == int(device_id):
                    deviceSeries=series
                    break
        deviceSeries["series"].append({"umt":int(umt),"value":value})
        return resultSeries
        



    def __del__(self):
        not self._quiet and print("__del__")
        self._cur.close()
        self._conn.close()





