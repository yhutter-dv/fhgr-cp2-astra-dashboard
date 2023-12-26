# Dotenv
from dotenv import dotenv_values
# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Influx DB
from influxdb_client import InfluxDBClient, Point 
from influxdb_client.client.write_api import SYNCHRONOUS
# Schedule
from apscheduler.schedulers.background import BackgroundScheduler

import os
import json
import sys
import time
from random import random
from datetime import datetime

class DetectorMeasurement(BaseModel):
    id: str
    index: int

class DetectorMeasurementsBody(BaseModel):
    detectorMeasurements: list[DetectorMeasurement]
    time: str = "-4h"

class StationsBody(BaseModel):
    canton: str | None = ""
    
def read_mst_from_file():
    with open("./data/mst.json", "r") as f:
        mst = json.load(f)
    return mst


def read_msr_from_file():
    with open("./data/msr.json", "r") as f:
        msr = json.load(f)
    return msr

def create_app():
    app = FastAPI()

    # Allow CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

def connect_to_db():
    try:
        token = config["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"]
        org = config["DOCKER_INFLUXDB_INIT_ORG"]
        url = config["INFLUXDB_URL"]

        print(f"Connecting to InfluxDB with the following configuration\n token => {token}\n org => {org}\n url => {url}")
        write_client = InfluxDBClient(url=url, token=token, org=org)
    except Exception as error:
        sys.exit(f"Error in connecting to InfluxDB, reason: {error}")
    return write_client


def load_env_vars():
    if not os.path.isfile(env_file_path):
        sys.exit(f"Expected file {env_file_path} to be available but it was not found...")
    else:
        print(f"Found env file {env_file_path}...")
    config = dotenv_values(env_file_path)
    return config

def write_detector_measurements_from_msr(msr):
    try:
        with db_client.write_api(write_options=write_options) as api:
            detector_measurements = []
            for detector_measurement in msr["detector_measurements"]:
                for sensor_measurement in detector_measurement["sensorMeasurements"]:
                    data = {
                        "measurement": "detector_measurement",
                        "tags": {
                            "id": detector_measurement["id"],
                            "index": int(sensor_measurement["index"]),
                            "hasError": bool(sensor_measurement["hasError"]),
                            "canton": detector_measurement.get("canton", "none")
                        },
                        "fields": {
                            "value": float(sensor_measurement["value"] + random() * 10),
                            "numberOfInputValuesUsed": int(sensor_measurement.get("numberOfInputValuesUsed", 0)),
                            "errorReason": sensor_measurement.get("errorReason", "none")
                        },
                        "time": datetime.utcnow()
                    }
                    detector_measurements.append(data)
            print(f"Writing {len(detector_measurements)} detector measurements into db...")
            api.write(bucket=bucket, org=db_client.org, record=detector_measurements)
            print("Finished...")
    except Exception as error:
        print(f"Failed to write MSR data because {error}")

def update_detector_measurements_in_db():
    # TODO: Read via webrequest instead of static file...
    msr = read_msr_from_file()
    write_detector_measurements_from_msr(msr)

def create_query_from_template(template, placeholder, elements, operator):
        query = ""
        for index, element in enumerate(elements):
            if index < len(elements) - 1:
                # Only append or if not last element.
                query += template.replace(placeholder, str(element)) + operator + " " 
            else:
                query += template.replace(placeholder, str(element))
        return query

# Global variables

env_file_path = "./.env-local"
write_options = SYNCHRONOUS

bucket = "fhgr-cp2-bucket"
update_detector_measurements_in_db_interval_seconds = '*/5' # CRON Job notation, e.g every 20 seconds

app = create_app()
config = load_env_vars()
db_client = connect_to_db()
stations = read_mst_from_file()
cantons = list(set([station["canton"] for station in stations]))

@app.on_event("startup")
def on_startup():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_detector_measurements_in_db, 'cron', second=update_detector_measurements_in_db_interval_seconds)
    scheduler.start()

@app.on_event("shutdown")
def on_shutdown():
    # Close db client
    db_client.close()

@app.post("/stations")
async def post_stations(stationsBody: StationsBody):
    if stationsBody.canton == "" or stationsBody.canton == None:
        return stations
    filtered_stations = [station for station in stations if station["canton"] == stationsBody.canton]
    return filtered_stations

@app.post("/detector_measurements")
async def post_detector_measurements(detectorMeasurementsBody: DetectorMeasurementsBody):
    try:
        api = db_client.query_api()
        detector_measurements = detectorMeasurementsBody.detectorMeasurements
        time_str = detectorMeasurementsBody.time

        detector_measurements_result = []
        for detector_measurement in detector_measurements:
            id = detector_measurement.id
            index = detector_measurement.index
            query = """
                from(bucket: "fhgr-cp2-bucket")
                  |> range(start: %time%)
                  |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                  |> filter(fn: (r) => r["index"] == "%index%")
                  |> filter(fn: (r) => r["id"] == "%id%")
                  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
            query = query.replace("%time%", time_str).replace("%index%", str(index)).replace("%id%", id)
            print(f"Sending the following query {query}")
            records = api.query_stream(query)
            measurements = []
            for record in records:
                measurement = {
                    "value": record["value"],
                    "time": record["_time"],
                    "numberOfInputValuesUsed": record["numberOfInputValuesUsed"],
                    "errorReason": None if record["errorReason"] == "none" else record["errorReason"],
                    "hasError": False if record["hasError"] == "False" else True
                }
                measurements.append(measurement)
            detector_measurement = {
                "id": id,
                "measurements": measurements
            }
            detector_measurements_result.append(detector_measurement)
        return detector_measurements_result
    except Exception as error:
        print(f"Failed to get detector measurements because {error}")
        return []

@app.get("/cantons")
async def get_cantons():
    return cantons
    
