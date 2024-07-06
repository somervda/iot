#!/usr/bin/python3

import psycopg

class Dbiot:

    _quiet = True
    _conn = None
    _cur = None

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self._conn = psycopg.connect("dbname=iotdb user=pi")
        self._cur = self._conn.cursor()

    def listTable(self,sql):
        not self._quiet and print("listTable",sql)
        self._cur.execute(sql)
        return self._cur.fetchall()


    def __del__(self):
        not self._quiet and print("__del__")
        self._cur.close()
        self._conn.close()





