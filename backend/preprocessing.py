from lxml import etree as etree_lxml
import os
import json
import requests
from dotenv import dotenv_values
import csv
import sys
from pyproj import Transformer

def ensure_file(file_path):
    if not os.path.isfile(file_path):
        sys.exit(f"Expected file '{file_path}' but was not found...")

def convert_east_north_to_long_lat(east_lv95, north_lv95):
    lat, lon = TRANSFORMER.transform(east_lv95, north_lv95)
    return (lon, lat)

def load_detector_names():
    ensure_file(DETECTOR_NAMES_FILE_PATH)
    # Build up dictionary where the name of the detector can be retrieved by id
    detector_names = {}
    with open(DETECTOR_NAMES_FILE_PATH, 'r', encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # skip header
        for row in csv_reader:
            lcd, rnid, n1id, n2id, name  = row
            detector_names[lcd] = name
    return detector_names

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


MST_LOCATIONS_FILE_PATH = "./data/mst_locations.csv"
MST_FILE_PATH = "./data/mst.json"
MSR_FILE_PATH = "./data/msr.json"
PAYLOAD_MST_FILE_PATH = "./data/payload_pull_mst.xml"
PAYLOAD_MSR_FILE_PATH = "./data/payload_pull_msr.xml"
DETECTOR_NAMES_FILE_PATH = "./data/detector_names.csv"
ENV_FILE_PATH = "./.env-local"
SECRETS = dotenv_values(ENV_FILE_PATH)

# Load the detector names which will be mapped to the detectors of each individual stations
DETECTOR_NAMES = load_detector_names()
# Load the mapping so we know which detector id is mapped to which canton
DETECTOR_ID_TO_CANTON_MAPPING = load_detector_id_to_canton_mapping()

# Needed to convert from Swiss LV95 coordinate system to WGS84 (Longitude, Latitude)
TRANSFORMER = Transformer.from_crs("EPSG:2056", "EPSG:4326")

def detector_id_to_station_id(detector_id):
    # Dectector Id: CH:0002.01
    # Station Id: CH:0002
    return detector_id.split(".")[0]


def station_id_to_number_id(station_id):
    # Station Id: CH:0002
    # Number Id: 2
    return int(station_id.split(":")[1])

def enrich_stations(stations):
    ensure_file(MST_LOCATIONS_FILE_PATH)
    # Build up a lookup table where information about a station can easily be retrieved by id
    mst_location_information = {}
    with open(MST_LOCATIONS_FILE_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            id = int(row["id"])
            mst_location_information[id] = {
                "name": row["description"],
                "canton": row["canton"],
                "eastLv95": int(row["east_lv95"]),
                "northLv95": int(row["north_lv95"])
            }

    # Enrich station with human readable names, location information and which canton they belong to
    for station in stations:
        station_id = station["numberId"]
        mst_location_information_for_station = mst_location_information[station_id]
        eastLv95 = mst_location_information_for_station["eastLv95"]
        northLv95 = mst_location_information_for_station["northLv95"]
        longitude, latitude = convert_east_north_to_long_lat(eastLv95, northLv95)
        station["name"] = mst_location_information_for_station["name"]
        station["canton"] = mst_location_information_for_station["canton"]
        station["eastLv95"] = eastLv95
        station["northLv95"] = northLv95
        station["longitude"] = longitude
        station["latitude"] = latitude

    return stations

def parse_mst(xml_content):
    # Load the xml content into a etree structure which
    # can be queried with XPath expressions
    tree = etree_lxml.fromstring(xml_content)
    ns = {
        "dx223": "http://datex2.eu/schema/2/2_0",
    }

    # Only select Records from ASTRA (CH)
    detector_id_nodes = tree.xpath(
        './/dx223:measurementSiteRecord[starts-with(@id, "CH")]',
        namespaces=ns)

    stations = list(dict())
    current_station_id = ""
    last_station_id = ""
    current_station = {}
    for node in detector_id_nodes:
        current_station_id = detector_id_to_station_id(node.attrib["id"])
        number_id = station_id_to_number_id(current_station_id)
        if current_station_id != last_station_id:
            if current_station:
                stations.append(current_station)

            last_station_id = current_station_id

            # Create a new station as we have a new id
            current_station = {"id": current_station_id,
                               "name": "",
                               "canton": "",
                               "numberId": number_id,
                               "eastLv95": None,
                               "northLv95": None,
                               "longitude": None,
                               "latitude": None,
                               "detectors": []
                               }

        # We are on the same station, looping over the detectors.
        # Each station can have up to 9 different detectors each with
        # individual characteristics.

        latitude_node = node.xpath(
            ".//dx223:pointCoordinates//dx223:latitude", namespaces=ns)[0]
        longitude_node = node.xpath(
            ".//dx223:pointCoordinates//dx223:longitude", namespaces=ns)[0]

        detector = {
            "id": node.attrib["id"],
            "characteristics": [],
            "latitude": float(latitude_node.text),
            "longitude": float(longitude_node.text)
        }

        characteristics = []

        # Select all characteristics with an index attribute available
        characteristic_nodes = node.xpath(
            ".//dx223:measurementSpecificCharacteristics[@index]", namespaces=ns)
        for characteristic_node in characteristic_nodes:
            characteristic = {}
            index = characteristic_node.attrib["index"]
            period_nodes = characteristic_node.xpath(
                ".//dx223:period", namespaces=ns)
            if len(period_nodes) > 0:
                characteristic["period"] = int(period_nodes[0].text)
            else:
                print(
                    f"Could not find a period for characteristic with index {index} for detector {detector['id']}")
                characteristic["period"] = -1
            measurement_nodes = characteristic_node.xpath(
                ".//dx223:specificMeasurementValueType", namespaces=ns)
            if len(measurement_nodes) > 0:
                characteristic["measurement"] = measurement_nodes[0].text
            else:
                print(
                    f"Could not find a measurement for characteristic with index {index} detector {detector['id']}")
                characteristic["measurement"] = None
            vehicle_type_nodes = characteristic_node.xpath(
                ".//dx223:vehicleType", namespaces=ns)
            if len(vehicle_type_nodes) > 0:
                characteristic["vehicleType"] = vehicle_type_nodes[0].text
            else:
                print(
                    f"Could not find a vehicle type characteristic with index {index} for detector {detector['id']}")
                characteristic["vehicleType"] = None

            characteristic["index"] = int(index)
            characteristics.append(characteristic)

        direction_nodes = node.xpath(
            ".//dx223:alertCDirectionCoded", namespaces=ns)
        if len(direction_nodes) > 0:
            detector["direction"] = direction_nodes[0].text
        else:
            print(
                f"Could not find a direction for detector {detector['id']}")
            detector["direction"] = None

        specific_location_id_nodes = node.xpath(
            ".//dx223:specificLocation", namespaces=ns)

        if len(specific_location_id_nodes) > 0:
            location_id = specific_location_id_nodes[0].text
            detector["locationId"] = int(location_id)
            detector["name"] = DETECTOR_NAMES.get(location_id, None)
        else:
            print(
                f"Could not find a location id for detector {detector['id']}")
            detector["locationId"] = -1

        detector["characteristics"] = characteristics
        current_station["detectors"].append(detector)

    stations.append(current_station)

    return enrich_stations(stations)

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


def parse_msr_from_request():
    token = SECRETS.get("OPEN_TRANSPORT_DATA_AUTH_TOKEN", "")
    if token == "":
        print("No token found, are you sure you created a '.env' file and specified a value for 'OPEN_TRANSPORT_DATA_AUTH_TOKEN'?")
        return

    ensure_file(PAYLOAD_MSR_FILE_PATH)

    with open(PAYLOAD_MSR_FILE_PATH, "r",) as f:
        payload = f.read()
    url = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        "Authorization": token,
        "SOAPAction": "http://opentransportdata.swiss/TDP/Soap_Datex2/Pull/v1/pullMeasuredData"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    result = parse_msr(response.text.encode())

    with open(MSR_FILE_PATH, "w") as f:
        json.dump(result, f, indent=4)

def parse_mst_from_request():
    token = SECRETS.get("OPEN_TRANSPORT_DATA_AUTH_TOKEN", "")
    if token == "":
        print("No token found, are you sure you created a '.env' file and specified a value for 'OPEN_TRANSPORT_DATA_AUTH_TOKEN'?")
        return

    ensure_file(PAYLOAD_MST_FILE_PATH)

    with open(PAYLOAD_MST_FILE_PATH, "r",) as f:
        payload = f.read()

    url = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        "Authorization": token,
        "SOAPAction": "http://opentransportdata.swiss/TDP/Soap_Datex2/Pull/v1/pullMeasurementSiteTable"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    result = parse_mst(response.text.encode())

    with open(MST_FILE_PATH, "w") as f:
        json.dump(result, f, indent=4)

def parse_msr_from_file():
    file_path = "./data/msr_sample.xml"
    ensure_file(file_path)

    with open(file_path, "rb") as f:
        xml_content = f.read()

    result = parse_msr(xml_content)

    with open(MSR_FILE_PATH, "w") as f:
        json.dump(result, f, indent=4)

def parse_mst_from_file():
    file_path = "./data/mst_sample.xml"
    ensure_file(file_path)

    with open(file_path, "rb") as f:
        xml_content = f.read()

    result = parse_mst(xml_content)

    with open(MST_FILE_PATH, "w") as f:
        json.dump(result, f, indent=4)



if __name__ == "__main__":
    # parse_mst_from_file()
    parse_mst_from_request()

    # parse_msr_from_file()
    parse_msr_from_request()
