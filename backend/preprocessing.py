from lxml import etree as etree_lxml
import os
import json
import requests
from dotenv import load_dotenv


def detector_id_to_station_id(detector_id):
    # Dectector Id: CH:0002.01
    # Station Id: CH:0002
    return detector_id.split(".")[0]


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
        if current_station_id != last_station_id:
            if current_station:
                stations.append(current_station)

            last_station_id = current_station_id

            # Create a new station as we have a new id
            current_station = {"id": current_station_id,
                               "east_lv95": "",
                               "north_lv95": "",
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
            "latitude": latitude_node.text,
            "longitude": longitude_node.text
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
                detector["period"] = period_nodes[0].text
            else:
                print(
                    f"Could not find a period for detector {detector['id']}")
                detector["period"] = ""
            measurement_nodes = characteristic_node.xpath(
                ".//dx223:specificMeasurementValueType", namespaces=ns)
            if len(measurement_nodes) > 0:
                detector["measurement"] = measurement_nodes[0].text
            else:
                print(
                    f"Could not find a measurement for detector {detector['id']}")
                detector["measurement"] = ""
            vehicle_type_nodes = characteristic_node.xpath(
                ".//dx223:vehicleType", namespaces=ns)
            if len(vehicle_type_nodes) > 0:
                detector["vehicleType"] = vehicle_type_nodes[0].text
            else:
                print(
                    f"Could not find a vehicle type for detector {detector['id']}")
                detector["vehicleType"] = ""

            characteristic["index"] = int(index)
            characteristics.append(characteristic)

        direction_nodes = node.xpath(
            ".//dx223:alertCDirectionCoded", namespaces=ns)
        if len(direction_nodes) > 0:
            detector["direction"] = direction_nodes[0].text
        else:
            print(
                f"Could not find a direction for detector {detector['id']}")
            detector["direction"] = ""

        specific_location_id_nodes = node.xpath(
            ".//dx223:specificLocation", namespaces=ns)

        if len(specific_location_id_nodes) > 0:
            detector["locationId"] = specific_location_id_nodes[0].text
        else:
            print(
                f"Could not find a location id for detector {detector['id']}")
            detector["locationId"] = ""

        detector["characteristics"] = characteristics
        current_station["detectors"].append(detector)

    stations.append(current_station)

    # TODO: Enrich station with human readable name and canton information

    return stations


def parse_msr(xml_content):
    tree = etree_lxml.fromstring(xml_content)
    ns = {
        "dx223": "http://datex2.eu/schema/2/2_0",
    }

    # Only select Records from ASTRA (CH)
    site_measurement_nodes = tree.xpath(
        './/dx223:siteMeasurements',
        namespaces=ns)

    result = dict()
    measurements = []
    for node in site_measurement_nodes:
        current_measurement = {}

        id_node = node.xpath(
            './/dx223:measurementSiteReference[@id]', namespaces=ns)[0]

        time_node = node.xpath(
            './/dx223:measurementTimeDefault', namespaces=ns)[0]

        current_measurement["id"] = id_node.attrib["id"]
        current_measurement["time"] = time_node.text
        measurements.append(current_measurement)

    result["measurements"] = measurements
    return result


def parse_mst_from_request():
    token = os.getenv(
        "OPEN_TRANSPORT_DATA_AUTH_TOKEN", "")
    if token == "":
        print("No token found, are you sure you created a '.env' file and specified a value for 'OPEN_TRANSPORT_DATA_AUTH_TOKEN'?")
        return

    with open("./data/payload_pull_mst.xml", "r",) as f:
        payload = f.read()
    url = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        "Authorization": token,
        "SOAPAction": f"{url}/v1/pullMeasurementSiteTable"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return parse_mst(response.text.encode())


def parse_mst_from_file(file_path):
    if not os.path.isfile(file_path):
        print(f"Could not open file '{file_path}'")
        return

    with open(file_path, "rb") as f:
        xml_content = f.read()

    return parse_mst(xml_content)


def parse_msr_from_file(file_path):
    if not os.path.isfile(file_path):
        print(f"Could not open file '{file_path}'")
        return

    with open(file_path, "rb") as f:
        xml_content = f.read()

    return parse_msr(xml_content)


def create_detector_to_measurement_type_map(mst_file_path):
    if not os.path.isfile(mst_file_path):
        print(f"Could not read file {mst_file_path}")
        return

    with open(mst_file_path, "r") as f:
        stations = json.load(f)


def demo_parse_mst_from_file():
    file_path = "./data/mst_sample.xml"
    output_path = "./data/mst.json"
    stations = parse_mst_from_file(file_path)

    with open(output_path, "w") as f:
        json.dump(stations, f, indent=4)


def demo_parse_mst_from_request():
    output_path = "./data/mst.json"
    stations = parse_mst_from_request()

    with open(output_path, "w") as f:
        json.dump(stations, f, indent=4)


def demo_parse_msr_from_file():
    file_path = "./data/msr_sample.xml"
    output_path = "./data/msr.json"
    stations = parse_msr_from_file(file_path)

    with open(output_path, "w") as f:
        json.dump(stations, f, indent=4)


if __name__ == "__main__":
    # Required in order to access environment variables
    load_dotenv()
    demo_parse_mst_from_file()
    # demo_parse_mst_from_request()
    # demo_parse_msr_from_file()
