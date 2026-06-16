from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path
from typing import List

app = FastAPI(
    title="Customer Retention API",
    version="1.0"
)
#  Multi doc attach ANalytics Local Check -->> Deploy Same 


BASE_DIR = Path(__file__).resolve().parent

# kmeans = joblib.load(BASE_DIR / "model" / "kmeans_model.pkl")
# scaler = joblib.load(BASE_DIR / "model" / "scaler.pkl")
kmeans = joblib.load(BASE_DIR / "kmeans_model.pkl")
scaler = joblib.load(BASE_DIR / "scaler.pkl")

segment_map = {
    0: "Low-Value Passive Customers",
    1: "Loyal High-Value Customers",
    2: "Deal-Driven Active Customers"
}

cluster_description = {
    0: "Low spending and low engagement customers.",
    1: "Highly valuable and loyal customers.",
    2: "Price-sensitive but active customers."
}


class CustomerInput(BaseModel):

    Recency: int
    Total_Spending: float
    NumWebPurchases: int
    NumStorePurchases: int
    NumCatalogPurchases: int
    NumDealsPurchases: int
    NumWebVisitsMonth: int
    Income: float
    Age: int

class CustomerBatchInput(BaseModel):
    data: List[CustomerInput]

def calculate_r_score(recency):
    if recency <= 30:
        return 5
    elif recency <= 60:
        return 4
    elif recency <= 90:
        return 3
    elif recency <= 120:
        return 2
    return 1


def calculate_f_score(frequency):
    if frequency >= 20:
        return 5
    elif frequency >= 15:
        return 4
    elif frequency >= 10:
        return 3
    elif frequency >= 5:
        return 2
    return 1


def calculate_m_score(spending):
    if spending >= 2000:
        return 5
    elif spending >= 1500:
        return 4
    elif spending >= 1000:
        return 3
    elif spending >= 500:
        return 2
    return 1


def risk_level(risk_pct):
    if risk_pct >= 70:
        return "High Risk"
    elif risk_pct >= 40:
        return "Medium Risk"
    return "Low Risk"


def retention_action(segment, risk):

    if risk == "High Risk":

        if segment == "Loyal High-Value Customers":
            return "VIP retention"

        elif segment == "Deal-Driven Active Customers":
            return "Discount campaigns"

        return "Win-back campaign"

    elif risk == "Medium Risk":
        return "Engagement nudges"

    return "Loyalty rewards"


@app.get("/")
def home():
    return {"message": "Customer Retention API Running"}


@app.post("/predict")
def predict(customer: CustomerInput):

    input_data = customer.dict()

    total_purchases = (
        input_data["NumWebPurchases"]
        + input_data["NumStorePurchases"]
        + input_data["NumCatalogPurchases"]
    )

    input_data["Total_Purchases"] = total_purchases

    df = pd.DataFrame([input_data])

    model_features = scaler.feature_names_in_

    df_model = df.reindex(columns=model_features)

    scaled = scaler.transform(df_model)

    cluster = int(kmeans.predict(scaled)[0])

    segment = segment_map[cluster]

    r = calculate_r_score(input_data["Recency"])
    f = calculate_f_score(total_purchases)
    m = calculate_m_score(input_data["Total_Spending"])

    rfm_score = r + f + m

    risk_pct = round((1 - (rfm_score / 15)) * 100, 2)

    risk = risk_level(risk_pct)

    action = retention_action(segment, risk)

    return {
        "cluster": cluster,
        "segment": segment,
        "rfm_score": rfm_score,
        "risk_percentage": risk_pct,
        "risk_level": risk,
        "recommendation": action,
        "description": cluster_description[cluster]
    }
@app.post("/batch_predict")
def batch_predict(payload: CustomerBatchInput):

    results = []

    for customer in payload.data:

        input_data = customer.dict()

        total_purchases = (
            input_data["NumWebPurchases"]
            + input_data["NumStorePurchases"]
            + input_data["NumCatalogPurchases"]
        )

        input_data["Total_Purchases"] = total_purchases

        df = pd.DataFrame([input_data])

        model_features = scaler.feature_names_in_
        df_model = df.reindex(columns=model_features)

        scaled = scaler.transform(df_model)

        cluster = int(kmeans.predict(scaled)[0])
        segment = segment_map[cluster]

        r = calculate_r_score(input_data["Recency"])
        f = calculate_f_score(total_purchases)
        m = calculate_m_score(input_data["Total_Spending"])

        rfm_score = r + f + m
        risk_pct = round((1 - (rfm_score / 15)) * 100, 2)
        risk = risk_level(risk_pct)
        action = retention_action(segment, risk)

        results.append({
            "cluster": cluster,
            "segment": segment,
            "rfm_score": rfm_score,
            "risk_level": risk,
            "risk_percentage": risk_pct,
            "recommendation": action
        })

    return results   # 👈 ONLY LIST (no JSON wrapper)