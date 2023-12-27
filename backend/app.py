# Dotenv
from dotenv import dotenv_values
# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
from request_models import *

def ensure_file(file_path):
    if not os.path.isfile(file_path):
        system.exit(f"Expected file '{file_path}' but was not found...")

def read_mst_from_file():
    ensure_file(MST_FILE_PATH)
    with open(MST_FILE_PATH, "r") as f:
        mst = json.load(f)
    return mst


def read_msr_from_file():
    ensure_file(MSR_FILE_PATH)
    with open(MSR_FILE_PATH, "r") as f:
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
        token = SECRETS["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"]
        org = SECRETS["DOCKER_INFLUXDB_INIT_ORG"]
        url = SECRETS["INFLUXDB_URL"]

        print(f"Connecting to InfluxDB with the following configuration\n token => {token}\n org => {org}\n url => {url}")
        write_client = InfluxDBClient(url=url, token=token, org=org)
    except Exception as error:
        sys.exit(f"Error in connecting to InfluxDB, reason: {error}")
    return write_client


def load_secrets():
    if not os.path.isfile(ENV_FILE_PATH):
        sys.exit(f"Expected file {ENV_FILE_PATH} to be available but it was not found...")
    else:
        print(f"Found env file {ENV_FILE_PATH}...")
    secrets = dotenv_values(ENV_FILE_PATH)
    return secrets

def write_detector_measurements_from_msr(msr):
    try:
        with db_client.write_api(write_options=WRITE_OPTIONS) as api:
            detector_measurements = []
            for detector_measurement in msr["detector_measurements"]:
                for sensor_measurement in detector_measurement["sensorMeasurements"]:
                    data = {
                        "measurement": "detector_measurement",
                        "tags": {
                            "id": detector_measurement["id"],
                            "index": int(sensor_measurement["index"]),
                            "hasError": bool(sensor_measurement["hasError"]),
                            "canton": detector_measurement.get("canton", "none"),
                            "stationId": detector_measurement.get("stationId", "none"),
                            "kind": "none" if sensor_measurement["kind"] == None else sensor_measurement["kind"]
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
            api.write(bucket=BUCKET, org=db_client.org, record=detector_measurements)
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
MSR_FILE_PATH = "./data/msr.json"
MST_FILE_PATH = "./data/mst.json"

ENV_FILE_PATH = "./.env-local"
WRITE_OPTIONS = SYNCHRONOUS

BUCKET = "fhgr-cp2-bucket"
UPDATE_DETECTOR_MEASUREMENTS_IN_DB_INTERVAL_SECONDS = '*/5' # CRON Job notation, e.g every 5 seconds
SECRETS = load_secrets()
MST = read_mst_from_file()
CANTONS = list(set([station["canton"] for station in MST]))

app = create_app()
db_client = connect_to_db()

@app.on_event("startup")
def on_startup():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_detector_measurements_in_db, 'cron', second=UPDATE_DETECTOR_MEASUREMENTS_IN_DB_INTERVAL_SECONDS)
    # scheduler.start()

@app.on_event("shutdown")
def on_shutdown():
    # Close db client
    db_client.close()

@app.post("/stations")
async def post_stations(stationsBody: StationsBody):
    stations = []
    has_canton = stationsBody.canton != None and stationsBody.canton != ""
    if not has_canton:
        # Do not filter stations
        stations = MST
    else:
        stations = [station for station in MST if station["canton"] == stationsBody.canton]

    # Query influx to get the number of errors for each station
    try:
        api = db_client.query_api()
        time_str = stationsBody.time

        number_of_errors_per_station = []

        query = ""
        if has_canton:
            query = """
                from(bucket: "fhgr-cp2-bucket")
                    |> range(start: %time%)
                    |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                    |> filter(fn: (r) => r["hasError"] == "True")
                    |> filter(fn: (r) => r["canton"] == "%canton%")
                    |> group(columns: ["stationId"])
                    |> count()
            """
            query = query.replace("%canton%", stationsBody.canton)
        else:
            # No canton specified
            query = """
                from(bucket: "fhgr-cp2-bucket")
                    |> range(start: %time%)
                    |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                    |> filter(fn: (r) => r["hasError"] == "True")
                    |> group(columns: ["stationId"])
                    |> count()
            """
        query = query.replace("%time%", time_str)
        print(f"Sending the following query {query}")
        records = api.query_stream(query)

        # Create dictionary with station id as key for fast look up
        station_id_to_error_number_mapping = {}
        for record in records:
            station_id = record["stationId"]
            number_of_errors = record["_value"]
            station_id_to_error_number_mapping[station_id] = number_of_errors

        # Add number_of_errors property to stations
        for station in stations:
            station_id = station["id"]
            # If the mapping returns 0 this means the station was not in the result set, e.g hasError was false. Therefore we can simply set the number to 0.
            station["numberOfErrors"] = station_id_to_error_number_mapping.get(station_id, 0)

        return stations
    except Exception as error:
        print(f"Failed to get stations because of {error}")
        return []

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
    return CANTONS

@app.post("/cantons/numberOfErrors")
async def get_cantons_number_of_errors(cantonNumberOfErrorsBody: CantonNumberOfErrorsBody):
    try:
        api = db_client.query_api()
        has_canton = cantonNumberOfErrorsBody.canton != None and cantonNumberOfErrorsBody.canton != ""
        canton = cantonNumberOfErrorsBody.canton
        time_str = cantonNumberOfErrorsBody.time

        query = ""
        if has_canton:
            query = """
                from(bucket: "fhgr-cp2-bucket")
                    |> range(start: %time%)
                    |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                    |> filter(fn: (r) => r["hasError"] == "True")
                    |> filter(fn: (r) => r["canton"] == "%canton%")
                    |> group(columns: ["canton"])
                    |> count()
            """
            query = query.replace("%canton%", canton)
        else:
            # No canton specified
            query = """
                from(bucket: "fhgr-cp2-bucket")
                    |> range(start: %time%)
                    |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                    |> filter(fn: (r) => r["hasError"] == "True")
                    |> group(columns: ["canton"])
                    |> count()
            """
        query = query.replace("%time%", time_str)
        print(f"Sending the following query {query}")
        cantons_number_of_errors = []
        records = api.query_stream(query)
        for record in records:
            canton_number_of_errors = {
                "canton": record["canton"],
                "numberOfErrors": record["_value"],
            }
            cantons_number_of_errors.append(canton_number_of_errors)
        return cantons_number_of_errors
    except Exception as error:
        print(f"Failed to get number of errors per canton because {error}")
        return []




@app.post("/station/numberOfErrors")
async def get_station_number_of_errors(stationNumberOfErrorsBody: CantonNumberOfErrorsBody):
    try:
        api = db_client.query_api()
        has_canton = stationNumberOfErrorsBody.canton != None and stationNumberOfErrorsBody.canton != ""
        canton = stationNumberOfErrorsBody.canton
        time_str = stationNumberOfErrorsBody.time

        query = ""
        if has_canton:
            # one canton specified, group by station
            query = """
                from(bucket: "fhgr-cp2-bucket")
                    |> range(start: %time%)
                    |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                    |> filter(fn: (r) => r["hasError"] == "True")
                    |> filter(fn: (r) => r["canton"] == "%canton%")
                    |> group(columns: ["stationId"])
                    |> count()
            """
            query = query.replace("%canton%", canton)
        else:
            # No canton specified, group by canton
            query = """
                from(bucket: "fhgr-cp2-bucket")
                    |> range(start: %time%)
                    |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                    |> filter(fn: (r) => r["hasError"] == "True")
                    |> group(columns: ["canton"])
                    |> count()
            """
        query = query.replace("%time%", time_str)
        print(f"Sending the following query {query}")
        stations_number_of_errors = []
        records = api.query_stream(query)
        for record in records:
            if has_canton:
                station_number_of_errors = {
                    "stationId": record["stationId"],
                    "numberOfErrors": record["_value"],
                }
                stations_number_of_errors.append(station_number_of_errors)
            else:
                station_number_of_errors = {
                    "canton": record["canton"],
                    "numberOfErrors": record["_value"],
                }
                stations_number_of_errors.append(station_number_of_errors)
        return stations_number_of_errors
    except Exception as error:
        print(f"Failed to get number of errors per station because {error}")
        return []
