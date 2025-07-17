import os
import sys
import certifi
import pymongo
import pandas as pd
import json

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from uvicorn import run as app_run

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constant.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)

# Load environment variables and MongoDB connection
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
ca = certifi.where()

client = pymongo.MongoClient(mongo_db_url, tlsCAFILE=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# FastAPI app setup
app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Templates
templates = Jinja2Templates(directory='templates')

# Load model and preprocessor
preprocessor = load_object("final_model/preprocessor.pkl")
final_model = load_object("final_model/model.pkl")
network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

# ---------- ROUTES ----------

@app.get("/", tags=["Root"])
async def index():
    return RedirectResponse(url='/docs')

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict", response_class=HTMLResponse)
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        y_pred = network_model.predict(df.drop(columns=['Result']))
        df['predicted_column'] = y_pred

        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        print(f"[Prediction Error] {e}")
        raise NetworkSecurityException(e, sys)

@app.post("/predict-json", response_class=JSONResponse)
async def predict_json_route(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df.drop(columns=['Result']))
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        return JSONResponse(content={"predictions": y_pred.tolist()})
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/upload-json-file", response_class=HTMLResponse)
async def upload_json_file(request: Request, file: UploadFile = File(...)):
    try:
        contents = await file.read()  # Read once, bytes
        # Now you can parse JSON multiple times from contents variable
        data1 = json.loads(contents)
        data2 = json.loads(contents)  # You can do this again safely

        # Do something with data1 or data2
        return templates.TemplateResponse("json_to_table.html", {"request": request, "data": data1})
    except Exception as e:
        return HTMLResponse(f"<h3>Error processing JSON file: {e}</h3>", status_code=400)


# ---------- ENTRY POINT ----------

if __name__ == '__main__':
    app_run(app, host="localhost", port=8000)
