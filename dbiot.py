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

    def addMeasurement(self, umt,application_id,device_id,data,adjustEpoch=False):
        not self._quiet and print("addMeasurement",umt,application_id,device_id,data,adjustEpoch)
        # umt is Universal Metric Time in seconds since 1Jan1970 (UNIX epoch)
        if adjustEpoch:
            # micropython frequently uses a epoch start of 1Jan2000, this flag
            # will change the value to a unix epoch
            umt += 946684800 
        sql = ("INSERT INTO measurement (umt,application_id,device_id,data) VALUES (%s, %s,%s,'%s')" %
            (umt,application_id,device_id,json.dumps(data)))
        not self._quiet and print("addMeasurement sql:",sql)
        result = self._cur.execute(sql)
        self._conn.commit()
        return result


    def __del__(self):
        not self._quiet and print("__del__")
        self._cur.close()
        self._conn.close()





