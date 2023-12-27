from pydantic import BaseModel

class DetectorMeasurement(BaseModel):
    id: str
    index: int

class DetectorMeasurementsBody(BaseModel):
    detectorMeasurements: list[DetectorMeasurement]
    time: str = "-4h" # Optional

class StationsBody(BaseModel):
    canton: str | None = "" # Optional
    time: str = "-4h" # Optional

class CantonNumberOfErrorsBody(BaseModel):
    canton: str | None = ""  # Optional
    time: str = "-4h" # Optional