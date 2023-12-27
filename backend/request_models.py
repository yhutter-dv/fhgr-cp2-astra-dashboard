from pydantic import BaseModel
from defaults import *

class DetectorMeasurement(BaseModel):
    id: str
    index: int

class DetectorMeasurementsBody(BaseModel):
    detectorMeasurements: list[DetectorMeasurement]
    time: str | None = DEFAULT_TIME_RANGE # Optional

class StationsBody(BaseModel):
    canton: str | None = "" # Optional
    time: str | None = DEFAULT_TIME_RANGE # Optional

class CantonNumberOfErrorsBody(BaseModel):
    canton: str | None = ""  # Optional
    time: str | None = DEFAULT_TIME_RANGE # Optional