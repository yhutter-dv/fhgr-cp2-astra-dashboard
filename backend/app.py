# Dotenv
from dotenv import dotenv_values
# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Influx DB
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import os
import json
import sys

debug = True

def read_mst_from_file():
    with open("./data/mst.json", "r") as f:
        mst = json.load(f)
    return mst

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

def create_db_client():
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "fhgr-cp2-org"
    url = "http://127.0.0.1:8086"

    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

    return write_client

def load_env_vars(debug):
    file_path = ".env-local" if debug else ".env"
    if not os.path.isfile(file_path):
        sys.exit(f"Expected file {file_path} to be available but it was not found...")
    else:
        print(f"Found env file {file_path}...")
    config = dotenv_values(file_path)
    return config


# Global variables
app = create_app()
config = load_env_vars(debug)
db_client = create_db_client()
mst = read_mst_from_file()
cantons = list(set([station["canton"] for station in mst]))

@app.get("/mst")
async def get_mst(canton: str = ""):
    if canton == "":
        return mst
    filtered_mst = [station for station in mst if station["canton"] == canton]
    return filtered_mst

@app.get("/cantons")
async def get_cantons():
    return cantons
    
