from dotenv import load_dotenv
from fastapi import FastAPI
import csv


def read_mst_locations():
    with open("./data/mst_locations.csv", "r", newline='') as f:
        reader = csv.DictReader(f, delimiter=";")
        mst_locations = [{
            "description": row["description"],
            "east_lv95": int(row["east_lv95"]),
            "north_lv95": int(row["north_lv95"]),
        } for row in reader]
    return mst_locations


load_dotenv()
app = FastAPI()
mst_locations = read_mst_locations()


@app.get("/mst_locations")
def mst_locations():
    return mst_locations
