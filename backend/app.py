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
import requests
# etree for fast xml parsing
from lxml import etree as etree_lxml

import os
import json
import sys
from datetime import datetime
from request_models import *
from defaults import *

def ensure_file(file_path):
    if not os.path.isfile(file_path):
        sys.exit(f"Expected file '{file_path}' but was not found...")

def read_mst_from_file():
    ensure_file(MST_FILE_PATH)
    with open(MST_FILE_PATH, "r") as f:
        mst = json.load(f)
    return mst

def detector_id_to_station_id(detector_id):
    # Dectector Id: CH:0002.01
    # Station Id: CH:0002
    return detector_id.split(".")[0]

def parse_msr(xml_content):
    tree = etree_lxml.fromstring(xml_content)
    ns = {
        "dx223": "http://datex2.eu/schema/2/2_0",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }

    site_measurement_nodes = tree.xpath(
        './/dx223:siteMeasurements',
        namespaces=ns)

    result = dict()
    detector_measurements = []
    for node in site_measurement_nodes:
        current_detector_measurement = {}
        current_sensor_measurements = []

        id_node = node.xpath(
            './/dx223:measurementSiteReference[@id]', namespaces=ns)[0]

        time_node = node.xpath(
            './/dx223:measurementTimeDefault', namespaces=ns)[0]

        measured_value_nodes = node.xpath(
            './/dx223:measuredValue[@index]', namespaces=ns)

        for measured_value_node in measured_value_nodes:
            index = int(measured_value_node.attrib["index"])
            current_sensor_measurement = {}
            measurement_kind = measured_value_node.xpath(
                './/dx223:basicData/@xsi:type', namespaces=ns)[0]

            has_data_error_nodes = measured_value_node.xpath(
                './/dx223:basicData//dx223:dataError', namespaces=ns)

            measured_value = 0
            error_reason = None
            kind = None
            has_data_error = len(has_data_error_nodes) > 0
            if has_data_error:
                error_reason_node = measured_value_node.xpath(
                    './/dx223:basicData//dx223:reasonForDataError//dx223:value', namespaces=ns)[0]
                error_reason = error_reason_node.text
            else:
                if measurement_kind == "dx223:TrafficFlow":
                    kind = "trafficFlow"
                    value_node = measured_value_node.xpath(
                        './/dx223:basicData//dx223:vehicleFlowRate', namespaces=ns)[0]
                    measured_value = float(value_node.text)
                elif measurement_kind == "dx223:TrafficSpeed":
                    kind = "trafficSpeed"
                    number_of_input_values_node = measured_value_node.xpath(
                        './/dx223:basicData//dx223:averageVehicleSpeed[@numberOfInputValuesUsed]', namespaces=ns)[0]

                    number_of_input_values_used = number_of_input_values_node.attrib[
                        "numberOfInputValuesUsed"]
                    value_node = measured_value_node.xpath(
                        './/dx223:basicData//dx223:speed', namespaces=ns)[0]
                    measured_value = float(value_node.text)
                    current_sensor_measurement["numberOfInputValuesUsed"] = int(
                        number_of_input_values_used)

            current_sensor_measurement["value"] = measured_value
            current_sensor_measurement["hasError"] = has_data_error
            current_sensor_measurement["errorReason"] = error_reason
            current_sensor_measurement["index"] = index
            current_sensor_measurement["kind"] = kind

            current_sensor_measurements.append(current_sensor_measurement)

        detector_id = id_node.attrib["id"]
        current_detector_measurement["id"] = detector_id
        current_detector_measurement["time"] = time_node.text
        current_detector_measurement["sensorMeasurements"] = current_sensor_measurements
        current_detector_measurement["canton"] = DETECTOR_ID_TO_CANTON_MAPPING.get(detector_id, None)
        current_detector_measurement["stationId"] = detector_id_to_station_id(detector_id)

        detector_measurements.append(current_detector_measurement)

    result["detector_measurements"] = detector_measurements
    return result

def load_detector_id_to_canton_mapping():
    ensure_file(MST_FILE_PATH)
    detector_id_canton_mapping = {}
    with open(MST_FILE_PATH, "r") as f:
        stations = json.load(f)
    for station in stations:
        for detector in station["detectors"]:
            detector_id = detector["id"]
            canton = station["canton"]
            detector_id_canton_mapping[detector_id] = canton
    return detector_id_canton_mapping

def parse_msr_from_request():
    url = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        "Authorization": TOKEN,
        "SOAPAction": "http://opentransportdata.swiss/TDP/Soap_Datex2/Pull/v1/pullMeasuredData"
    }
    response = requests.request("POST", url, headers=headers, data=MSR_PAYLOAD)
    result = parse_msr(response.text.encode())
    return result

def load_msr_payload_and_token():
    token = SECRETS.get("OPEN_TRANSPORT_DATA_AUTH_TOKEN", "")
    if token == "":
        print("No token found, are you sure you created a '.env' file and specified a value for 'OPEN_TRANSPORT_DATA_AUTH_TOKEN'?")
        return

    ensure_file(PAYLOAD_MSR_FILE_PATH)

    payload = ""
    with open(PAYLOAD_MSR_FILE_PATH, "r",) as f:
        payload = f.read()

    return (payload, token)

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
                            "value": float(sensor_measurement["value"]),
                            "numberOfInputValuesUsed": int(sensor_measurement.get("numberOfInputValuesUsed", 0)),
                            "errorReason": "none" if sensor_measurement["errorReason"] == None else sensor_measurement["errorReason"]
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
    try:
        msr = parse_msr_from_request()
        write_detector_measurements_from_msr(msr)
    except Exception as error:
        print(f"Failed to get latest msr data because of {error}")

def create_query_from_template(template, placeholder, elements, operator):
        query = ""
        for index, element in enumerate(elements):
            if index < len(elements) - 1:
                # Only append or if not last element.
                query += template.replace(placeholder, str(element)) + operator + " " 
            else:
                query += template.replace(placeholder, str(element))
        return query

def get_value_or_default(value, default):
    if value == None or value == "":
        return default
    return value

# Global variables
MSR_FILE_PATH = "./data/msr.json"
MST_FILE_PATH = "./data/mst.json"
PAYLOAD_MSR_FILE_PATH = "./data/payload_pull_msr.xml"


ENV_FILE_PATH = "./.env-local"
WRITE_OPTIONS = SYNCHRONOUS

UPDATE_DETECTOR_MEASUREMENTS_IN_DB_INTERVAL_MINUTES = '*/1  ' # CRON Job notation, e.g every 1 Minute
SECRETS = load_secrets()
BUCKET = SECRETS["DOCKER_INFLUXDB_INIT_BUCKET"]

MST = read_mst_from_file()
MSR_PAYLOAD, TOKEN = load_msr_payload_and_token()
# Load the mapping so we know which detector id is mapped to which canton
DETECTOR_ID_TO_CANTON_MAPPING = load_detector_id_to_canton_mapping()

ALL_CANTONS = "all"
CANTON_NAMES = list(set([station["canton"] for station in MST]))
CANTONS = [{
    "label": "All Cantons",
    "value": ALL_CANTONS
}]

CANTONS += [{"label": canton_name, "value": canton_name} for canton_name in CANTON_NAMES]

app = create_app()
db_client = connect_to_db()

@app.on_event("startup")
def on_startup():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_detector_measurements_in_db, 'cron', minute=UPDATE_DETECTOR_MEASUREMENTS_IN_DB_INTERVAL_MINUTES)
    # scheduler.start()

@app.on_event("shutdown")
def on_shutdown():
    # Close db client
    db_client.close()

@app.post("/stations")
async def post_stations(stationsBody: StationsBody):
    stations = []
    all_cantons = stationsBody.canton == ALL_CANTONS
    print("Got ", stationsBody.canton)
    if all_cantons:
        # Do not filter stations
        print("Not filtering any cantons when doing stations request")
        stations = MST
    else:
        print("Filtering cantons when doing stations request")
        stations = [station for station in MST if station["canton"] == stationsBody.canton]

    # Query influx to get the number of errors for each station
    try:
        api = db_client.query_api()
        time_str = get_value_or_default(stationsBody.time, DEFAULT_TIME_RANGE)

        query = ""
        if ALL_CANTONS:
            query = """
                from(bucket: "%bucket%")
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
                from(bucket: "%bucket%")
                    |> range(start: %time%)
                    |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                    |> filter(fn: (r) => r["hasError"] == "True")
                    |> group(columns: ["stationId"])
                    |> count()
            """
        query = query.replace("%time%", time_str).replace("%bucket%", BUCKET)
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
        time_str = get_value_or_default(detectorMeasurementsBody.time, DEFAULT_TIME_RANGE)

        detector_measurements_result = []
        for detector_measurement in detector_measurements:
            id = detector_measurement.id
            name = detector_measurement.name
            index = detector_measurement.index
            query = """
                from(bucket: "%bucket%")
                  |> range(start: %time%)
                  |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                  |> filter(fn: (r) => r["index"] == "%index%")
                  |> filter(fn: (r) => r["id"] == "%id%")
                  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
            query = query.replace("%time%", time_str).replace("%index%", str(index)).replace("%id%", id).replace("%bucket%", BUCKET)
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
            result = {
                "id": id,
                "name": name,
                "measurements": measurements
            }
            detector_measurements_result.append(result)
        return detector_measurements_result
    except Exception as error:
        print(error)
        print(f"Failed to get detector measurements because {error}")
        return []

@app.get("/cantons")
async def get_cantons():
    return CANTONS

@app.post("/cantons/total_number_of_errors")
async def post_cantons_total_number_of_errors(cantonTotalNumberOfErrorsBody: CantonTotalNumberOfErrorsBody):
    try:
        api = db_client.query_api()
        has_canton = cantonTotalNumberOfErrorsBody.canton != None and cantonTotalNumberOfErrorsBody.canton != ""
        canton = cantonTotalNumberOfErrorsBody.canton
        time_str = get_value_or_default(cantonTotalNumberOfErrorsBody.time, DEFAULT_TIME_RANGE)

        query = ""
        if has_canton:
            query = """
                from(bucket: "%bucket%")
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
                from(bucket: "%bucket%")
                    |> range(start: %time%)
                    |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                    |> filter(fn: (r) => r["hasError"] == "True")
                    |> group(columns: ["canton"])
                    |> count()
            """
        query = query.replace("%time%", time_str).replace("%bucket%", BUCKET)
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
        print(f"Failed to get total number of errors per canton because {error}")
        return []


@app.post("/cantons/number_of_errors")
async def post_cantons_number_of_errors(cantonNumberOfErrorsBody: CantonNumberOfErrorsBody):
    try:
        api = db_client.query_api()
        has_canton = cantonNumberOfErrorsBody.canton != None and cantonNumberOfErrorsBody.canton != ""
        canton = cantonNumberOfErrorsBody.canton.strip()
        time_str = get_value_or_default(cantonNumberOfErrorsBody.time, DEFAULT_TIME_RANGE)
        bin_size  = cantonNumberOfErrorsBody.binSize

        query = ""
        if not has_canton:
            return []
        
        if canton == ALL_CANTONS:
            query = """
            from(bucket: "%bucket%")
                |> range(start: %time%)
                |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                |> filter(fn: (r) => r["hasError"] == "True")
                |> window(every: %bin_size%)
                |> count()
                |> group(columns: ["_time", "canton"])
                |> duplicate(column: "_stop", as: "_time")
                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
        else:
            # Specific canton specified
            query = """
                 from(bucket: "%bucket%")
                    |> range(start: %time%)
                    |> filter(fn: (r) => r["_measurement"] == "detector_measurement")
                    |> filter(fn: (r) => r["hasError"] == "True")
                    |> filter(fn: (r) => r["canton"] == "%canton%")
                    |> window(every: %bin_size%)
                    |> count()
                    |> group(columns: ["_time", "canton"])
                    |> duplicate(column: "_stop", as: "_time")
                    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
            query = query.replace("%canton%", canton)

        query = query.replace("%time%", time_str).replace("%bin_size%", bin_size).replace("%bucket%", BUCKET)
        print(f"Sending the following query {query}")
        cantons_number_of_errors = []
        tables = api.query(query)
        
        # We get a table result because we window by the bin size
        for table in tables:
            # We can get the canton from any of the records as it is ensure that all records in the same
            # Table do have the same canton (because we grouped by it)
            canton_result = {
                "name": table.records[0]["canton"]
            }
            measurements = []
            for record in table.records:
                measurement = {
                    "numberOfErrors": record["value"],
                    "time": record["_time"]
                }
                measurements.append(measurement)
            
            canton_result["measurements"] = measurements
            cantons_number_of_errors.append(canton_result)
        return cantons_number_of_errors
    except Exception as error:
        print(f"Failed to get number of errors per canton because {error}")
        return []