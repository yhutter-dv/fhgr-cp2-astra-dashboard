from pydantic import BaseModel

class DetectorMeasurement(BaseModel):
    id: str
    index: int

class DetectorMeasurementsBody(BaseModel):
    detectorMeasurements: list[DetectorMeasurement]
    time: str = "-4h"

class StationsBody(BaseModel):
    canton: str | None = ""