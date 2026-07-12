from pyexpat import features

from fastapi import FastAPI,Request
from models.report import Report
from database.operations import insert_sys_info, insert_resource_usage, get_system_id, get_all_alert , get_all_resource_usage , get_all_system , save_one_process , get_all_process , process_exists , delete_missing_processes , update_process, save_ml_prediction , get_latest_ml_prediction
from database.scheme import create_alert_table, create_table, create_resource_usage_table , create_process_table
from database.rules import resource_analyzer
from fastapi.middleware.cors import CORSMiddleware
from ml.feature_extractor import extract_features
from ml.predict import predict_risk
from ml.model_status import latest_prediction
app = FastAPI()

@app.on_event("startup")
def init_db():
    print("Creating sys_info...")
    create_table()

    print("Creating resource_usage...")
    create_resource_usage_table()

    print("Creating alert_table")
    create_alert_table()

    print("Creating process_table")
    create_process_table()

@app.get("/")
def home():
    return{
        "Hello" : "Welcome to the server"
    }



@app.post("/report")
def report(data: Report):

    insert_sys_info(data.system_info)

    sys_id = get_system_id(data.system_info.hostname)

    insert_resource_usage(
        sys_id,
        data.resource_usage
    )

    risk_label = resource_analyzer(
        sys_id,
        data.resource_usage
    )   
    active_pids = []

    for process in data.processes:
        active_pids.append(process.pid)
        if process_exists(sys_id, process.pid):
            update_process(sys_id, process)
        else:
            save_one_process(sys_id, process)
    delete_missing_processes(sys_id, active_pids)

    features = extract_features(data, sys_id)

    # Save dataset for future retraining
    features["risk_label"] = risk_label

    # AI Prediction
    prediction = predict_risk(features)

    save_ml_prediction(
        sys_id,
        prediction,
        100,
        "Random Forest",
        "1.0"
    )
    latest_prediction["prediction"] = prediction
    latest_prediction["confidence"] = 100
    latest_prediction["model"] = "Random Forest"
    latest_prediction["version"] = "1.0"

    print("=" * 40)
    print(f"Rule Engine : {risk_label}")
    print(f"AI Model    : {prediction}")
    print("=" * 40)

    return {
        "message": "Data received successfully!"
    }


@app.get("/systems")
def get_systems():
    return get_all_system()

@app.get("/resource-usage")
def get_resource_usage():
    return get_all_resource_usage()

@app.get("/alerts")
def get_alerts():
    return get_all_alert()

@app.get("/processes")
def get_processes():
    return get_all_process()

@app.get("/ml-status/{system_id}")
def get_ml_status(system_id: int):

    prediction = get_latest_ml_prediction(system_id)

    if prediction is None:
        return {
            "prediction": "UNKNOWN",
            "confidence": 0,
            "model": "Random Forest",
            "version": "1.0"
        }

    return prediction


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)