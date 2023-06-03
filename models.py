from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class PricePredictions(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    Day: int
    Month: int
    ForecastWindProduction: float
    SystemLoadEA: float
    SMPEA: float
    ORKTemperature: float
    ORKWindspeed: float
    CO2Intensity: float
    ActualWindProduction: float
    SystemLoadEP2: float
    prediction: float
    prediction_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    client_ip: str

class Price(SQLModel):
    Day: int
    Month: int
    ForecastWindProduction: float
    SystemLoadEA: float
    SMPEA: float
    ORKTemperature: float
    ORKWindspeed: float
    CO2Intensity: float
    ActualWindProduction: float
    SystemLoadEP2: float

    class Config:
        schema_extra = {
            "example": {
                "Day": 10,
                "Month": 12,
                "ForecastWindProduction": 54.10,
                "SystemLoadEA": 4241.05,
                "SMPEA":49.56,
                "ORKTemperature":9.0,
                "ORKWindspeed":14.8,
                "CO2Intensity":491.32,
                "ActualWindProduction":54.0,
                "SystemLoadEP2":4426.84

            }
        }

