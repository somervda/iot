#!/usr/bin/python3

import sys
import time
import asyncio
from dbiot import Dbiot



# fastAPI 
from typing import Union,Annotated
from fastapi import FastAPI,Path,Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

_quiet = False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/measurements/{application_id}/{device_id}/{timestamp}/{rows}")
def getMeasurements(application_id: Annotated[int, Path(title="application_id: Set of application metrics to collect", ge=1)],
    device_id: Annotated[int, Path(title="devices_id: Device filter 0=All", ge=0)], 
    timestamp: Annotated[int, Path(title="timestamp in seconds since 1Jan1970 to retrieve", ge=0)],
    rows: Annotated[int, Path(title="rows: Number of rows to retrieve", ge=1,le=1000)]):

    not _quiet and print("getMeasurements:",application_id,device_id,timestamp,rows)
    # get and return data
    db = Dbiot(quiet=False)
    sql = """select measurement.id,umt,to_timestamp(umt) as umtdate,data, 
            ((data->>'celsius')::numeric * 9/5) + 32 as fahrenheit,
            device_id,application_id,application.name,device.name from measurement 
            JOIN application ON measurement.application_id = application.id
            JOIN device ON measurement.device_id = device.id
            WHERE application_id = """ + str(application_id) 
    sql += "\nAND umt>=" + str(timestamp)
    if device_id != 0:
        sql += "\nAND device_id=" + str(device_id) 
    sql += "\nORDER BY umt desc"
    sql += "\nLIMIT " + str(rows)
    not _quiet and print("sql:",sql)
    iotData = db.listTable()
    db = None    
    return iotData




# Note: Make sure this line is at the end of the file so fastAPI falls through the other
# routes before serving up static files 
# static files contains the angular iot_ui application
app.mount("/", StaticFiles(directory="static", html=True), name="static")