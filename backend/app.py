from dotenv import load_dotenv
from fastapi import FastAPI
import json


def read_mst_from_file():
    with open("./data/mst.json", "r") as f:
        mst = json.load(f)
    return mst


load_dotenv()
app = FastAPI()
mst = read_mst_from_file()


@app.get("/mst")
async def mst_locations(canton: str = ""):
    if canton == "":
        return mst
    filtered_mst = [station for station in mst if station["canton"] == canton]
    return filtered_mst
