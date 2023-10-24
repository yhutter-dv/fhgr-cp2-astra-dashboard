import os
import requests
from lxml import etree as etree_lxml
import csv


class Mst():
    def __init__(self):
        self.OPENTRANSPORTDATA_TOKEN = os.getenv("OPEN_TRANSPORT_DATA_AUTH_TOKEN", "")
        with open("./data/payload_pull_mst.xml", "r",) as f:
            self.PULL_MST_PAYLOAD = f.read()
        self.OPENTRANSPORTDATA_PULL_URL = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"

        self.mst_locations = self.read_mst_locations()

    def read_mst_locations(self):
        with open("./data/mst_locations.csv", "r", newline='') as f:
            reader = csv.DictReader(f, delimiter=";")
            mst_locations = [{
                "description": row["description"],
                "east_lv95": int(row["east_lv95"]),
                "north_lv95": int(row["north_lv95"]),
            } for row in reader]
        return mst_locations

    def pull_mst(self):
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            "Authorization": self.OPENTRANSPORTDATA_TOKEN, 
            "SOAPAction": f"{self.OPENTRANSPORTDATA_PULL_URL}/v1/pullMeasurementSiteTable"
        }
        response = requests.request("POST", self.OPENTRANSPORTDATA_PULL_URL, headers=headers, data=self.PULL_MST_PAYLOAD)
        return response.text

    def parse_mst(self):
        with open("./data/mst_static.xml", "rb") as f:
            xml_content = f.read()
        tree = etree_lxml.fromstring(xml_content)
        ns = {
            "dx223": "http://datex2.eu/schema/2/2_0",
        }
        latitude_nodes = tree.xpath(
                './/dx223:measurementSiteRecord[starts-with(@id, "CH")]//dx223:pointCoordinates//dx223:latitude',
                namespaces=ns)
        latitudes = [node.text for node in latitude_nodes]

        id_nodes = tree.xpath(
                './/dx223:measurementSiteRecord[starts-with(@id, "CH")]',
                namespaces=ns)
        ids = [node.attrib["id"] for node in id_nodes]

        # TODO: This is currently WIP an not finished...
        # For starters we want to pass the content into this method instead of reading it
        # from a local file.

