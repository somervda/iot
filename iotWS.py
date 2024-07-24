#!/usr/bin/python3

# Note for testing 
# uvicorn iotWS:app --reload --host pi4.home

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


@app.get("/measurements/{application_id}/{device_id}/{timestamp}/{rows}/{grouping}")
def getRawMeasurements(application_id: Annotated[int, Path(title="application_id: Set of application metrics to collect", ge=1)],
    device_id: Annotated[int, Path(title="devices_id: Device filter 0=All", ge=0)], 
    timestamp: Annotated[int, Path(title="timestamp in seconds since 1Jan1970 to retrieve", ge=0)],
    rows: Annotated[int, Path(title="rows: Number of rows to retrieve", ge=1,le=1000)],
    grouping: Annotated[int, Path(title="grouping: 0=None, 1=hour,2=day,3=week,4=month,5=year", ge=0,le=9)]
    ):

    not _quiet and print("getRawMeasurements:",application_id,device_id,timestamp,rows,grouping)
    # get and return data
    db = Dbiot(quiet=False)
    iotData = db.getRawMeasurements(application_id,device_id,timestamp,rows,grouping)
    db = None    
    return iotData

@app.get("/flatmeasurements/{application_id}/{device_id}/{timestamp}/{rows}/{grouping}/{field}")
def getFlatMeasurementsField(application_id: Annotated[int, Path(title="application_id: Set of application metrics to collect", ge=1)],
    device_id: Annotated[int, Path(title="devices_id: Device filter 0=All", ge=0)], 
    timestamp: Annotated[int, Path(title="timestamp in seconds since 1Jan1970 to retrieve", ge=0)],
    rows: Annotated[int, Path(title="rows: Number of rows to retrieve", ge=1,le=1000)],
    grouping: Annotated[int, Path(title="grouping: 0=None, 1=hour,2=day,3=week,4=month,5=year", ge=0,le=9)],
    field: Annotated[str, Path(title="field name")]
    ):
    not _quiet and print("getFlatMeasurementsField:",application_id,device_id,timestamp,rows,grouping,field)
    db = Dbiot(quiet=False)
    iotData = db.getFlatMeasurements(application_id,device_id,timestamp,rows,grouping,field)
    db = None
    return iotData


@app.get("/devices")
def getDevices():
    not _quiet and print("getDevices")
    # get and return data
    db = Dbiot(quiet=False)
    sql = "select * from device"
    devices = db.listTable(sql)
    db = None    
    return devices
    
@app.get("/device/{device_id}")
def getDevice(device_id: Annotated[int, Path(title="device_id: Device selector", ge=1)]):
    not _quiet and print("getDevice",device_id)
    # get and return data
    db = Dbiot(quiet=False)
    sql = "select * from device where id=" + str(device_id)
    device = db.listTable(sql)
    db = None    
    return device

@app.get("/applications")
def getApplications():
    not _quiet and print("getApplications")
    # get and return data
    db = Dbiot(quiet=False)
    sql = "select * from application"
    applications = db.listTable(sql)
    db = None    
    return applications
    
@app.get("/application/{application_id}")
def getDevice(application_id: Annotated[int, Path(title="application_id: Application selector", ge=1)]):
    not _quiet and print("getApplication",application_id)
    # get and return data
    db = Dbiot(quiet=False)
    sql = "select * from application where id=" + str(application_id)
    application = db.listTable(sql)
    db = None    
    return application


# Note: Make sure this line is at the end of the file so fastAPI falls through the other
# routes before serving up static files 
# static files contains the angular iot_ui application
app.mount("/", StaticFiles(directory="static", html=True), name="static")