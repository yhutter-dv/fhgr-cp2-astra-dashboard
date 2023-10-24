from mst import Mst
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI() 
mst = Mst()

@app.get("/mst_locations")
def mst_locations():
    return mst.mst_locations

