from pydantic import BaseModel
import datetime

class PredictRequest(BaseModel):
    lat: float
    lon: float
    date: datetime.date