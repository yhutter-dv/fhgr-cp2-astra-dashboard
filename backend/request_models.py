from pydantic import BaseModel
from defaults import *

class DetectorMeasurement(BaseModel):
    id: str
    index: int
    name: str | None = ""

class DetectorMeasurementsBody(BaseModel):
    detectorMeasurements: list[DetectorMeasurement]
    time: str | None = DEFAULT_TIME_RANGE # Optional

class StationsBody(BaseModel):
    canton: str | None = "" # Optional
    time: str | None = DEFAULT_TIME_RANGE # Optional

class CantonTotalNumberOfErrorsBody(BaseModel):
    canton: str | None = ""  # Optional
    time: str | None = DEFAULT_TIME_RANGE # Optional

class CantonNumberOfErrorsBody(BaseModel):
    canton: str | None = ""  # Optional
    binSize: str
    time: str | None = DEFAULT_TIME_RANGE # Optional