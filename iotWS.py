#!/usr/bin/python3

# Note for testing 
# uvicorn iotWS:app --reload --host pi3.home

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
def getMeasurements(application_id: Annotated[int, Path(title="application_id: Set of application metrics to collect", ge=1)],
    device_id: Annotated[int, Path(title="devices_id: Device filter 0=All", ge=0)], 
    timestamp: Annotated[int, Path(title="timestamp in seconds since 1Jan1970 to retrieve", ge=0)],
    rows: Annotated[int, Path(title="rows: Number of rows to retrieve", ge=1,le=1000)],
    grouping: Annotated[int, Path(title="grouping: 0=None, 1=hour,2=day,3=week,4=month,5=year", ge=0,le=5)]
    ):

    not _quiet and print("getMeasurements:",application_id,device_id,timestamp,rows)
    # get and return data
    db = Dbiot(quiet=False)
    iotData = db.getMeasurements(application_id,device_id,timestamp,rows,uvicorn iotWS:app --reload --host pi3.homeuvicorn iotWS:app --reload --host pi3.homegrouping)
    db = None    
    return iotData




# Note: Make sure this line is at the end of the file so fastAPI falls through the other
# routes before serving up static files 
# static files contains the angular iot_ui application
app.mount("/", StaticFiles(directory="static", html=True), name="static")