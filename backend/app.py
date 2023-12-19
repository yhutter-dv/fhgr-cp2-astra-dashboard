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

class DetectorMeasurementsBody(BaseModel):
    ids: list[str]
    indices: list[int]
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
                            "hasError": bool(sensor_measurement["hasError"])
                        },
                        "fields": {
                            "value": float(sensor_measurement["value"] + random() * 10),
                            "numberOfInputValuesUsed": int(sensor_measurement.get("numberOfInputValuesUsed", 0)),
                            "errorReason": "none" if sensor_measurement["errorReason"] == None else sensor_measurement["errorReason"]
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
    # scheduler.start()

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
        ids = detectorMeasurementsBody.ids
        indices = detectorMeasurementsBody.indices
        time_str = detectorMeasurementsBody.time
        # Because the contains filter in influxdb is not the fastest thing in the world
        # we use a conditional OR for filtering indices and ids
        id_filter_template = 'r["id"] == "%id%" '
        id_filter_query = create_query_from_template(id_filter_template, "%id%", ids, "or")
        indices_filter_template = 'r["index"] == "%index%" '
        indices_filter_query = create_query_from_template(indices_filter_template, "%index%", indices, "or")
        query = """
            from(bucket: "fhgr-cp2-bucket")
              |> range(start: %time%)
              |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
              |> filter(fn: (r) => %id_filter_query%)
              |> filter(fn: (r) => %indices_filter_query%)
              |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        """
        query = query.replace("%time%", time_str).replace("%id_filter_query%", id_filter_query).replace("%indices_filter_query%", indices_filter_query)
        records = api.query_stream(query)
        measurements = []
        for record in records:
            measurement = {
                "value": record["value"],
                "id": record["id"],
                "index": record["index"],
                "time": record["_time"],
                "numberOfInputValuesUsed": record["numberOfInputValuesUsed"],
                "errorReason": record["errorReason"],
            }
            measurements.append(measurement)
        return measurements
    except Exception as error:
        print(f"Failed to get detector measurements because {error}")
        return []

@app.get("/cantons")
async def get_cantons():
    return cantons
    
