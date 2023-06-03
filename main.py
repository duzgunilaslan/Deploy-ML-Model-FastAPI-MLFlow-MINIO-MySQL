from fastapi import FastAPI, Depends, Request
from models import Price,PricePredictions
import os
from sqlalchemy.orm import Session
from mlflow.sklearn import load_model
from database import engine, get_db, create_db_and_tables

# Tell where is the tracking server and artifact server
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5001/'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000/'

# Learn, decide and get model from mlflow model registry
model_name = "RFElectricityPricePrediction"
model_version = 6
model = load_model(
    model_uri=f"models:/{model_name}/{model_version}"
)

app = FastAPI()

# Creates all the tables defined in models module
create_db_and_tables()


# Note that model will coming from mlflow
def makePrediction(model, request):
    # parse input from request
    Day = request["Day"]
    Month = request["Month"]
    ForecastWindProduction = request["ForecastWindProduction"]
    SystemLoadEA = request["SystemLoadEA"]
    SMPEA = request["SMPEA"]
    ORKTemperature = request["ORKTemperature"]
    ORKWindspeed = request["ORKWindspeed"]
    CO2Intensity = request["CO2Intensity"]
    ActualWindProduction = request["ActualWindProduction"]
    SystemLoadEP2 = request["SystemLoadEP2"]

    # Make an input vector
    features = [[Day,
                 Month,
                 ForecastWindProduction,
                 SystemLoadEA,
                 SMPEA,
                 ORKTemperature,
                 ORKWindspeed,
                 CO2Intensity,
                 ActualWindProduction,
                 SystemLoadEP2]]

    # Predict
    prediction = model.predict(features)

    return prediction[0]



# Insert Prediction information
def insertPrice(request, prediction, client_ip, db):
    newPrice = PricePredictions(
        Day = request["Day"],
        Month = request["Month"],
        ForecastWindProduction = request["ForecastWindProduction"],
        SystemLoadEA = request["SystemLoadEA"],
        SMPEA = request["SMPEA"],
        ORKTemperature = request["ORKTemperature"],
        ORKWindspeed = request["ORKWindspeed"],
        CO2Intensity = request["CO2Intensity"],
        ActualWindProduction = request["ActualWindProduction"],
        SystemLoadEP2 = request['SystemLoadEP2'],
        prediction=prediction,
        client_ip=client_ip
    )

    with db as session:
        session.add(newPrice)
        session.commit()
        session.refresh(newPrice)

    return newPrice



# Electirical Price Prediction endpoint
@app.post("/prediction/priceprediction")
async def predictPrice(request: Price, fastapi_req: Request,  db: Session = Depends(get_db)):
    prediction = makePrediction(model, request.dict())
    db_insert_record = insertPrice(request=request.dict(), prediction=prediction,
                                          client_ip=fastapi_req.client.host,
                                          db=db)
    return {"prediction": prediction, "db_record": db_insert_record}
