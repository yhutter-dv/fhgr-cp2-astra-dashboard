from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json


def read_mst_from_file():
    with open("./data/mst.json", "r") as f:
        mst = json.load(f)
    return mst

load_dotenv()
app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mst = read_mst_from_file()
cantons = [station["canton"] for station in mst]
# Filter out duplicates
cantons = list(set(cantons))

@app.get("/mst")
async def get_mst(canton: str = ""):
    if canton == "":
        return mst
    filtered_mst = [station for station in mst if station["canton"] == canton]
    return filtered_mst

@app.get("/cantons")
async def get_cantons():
    return cantons
