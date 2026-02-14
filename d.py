import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# -------------------------------
# Load Models
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent
kmeans = joblib.load(BASE_DIR / "kmeans_model.pkl")
scaler = joblib.load(BASE_DIR / "scaler.pkl")

# -------------------------------
# Segment Mapping
# -------------------------------

segment_map = {
    0: "Low-Value Passive Customers",
    1: "Loyal High-Value Customers",
    2: "Deal-Driven Active Customers"
}

cluster_description = {
    0: "Low spending and low engagement customers. Focus on win-back or low-cost retention.",
    1: "Highly valuable and loyal customers. Priority segment for retention and premium offers.",
    2: "Price-sensitive but active customers. Respond well to discounts and campaigns."
}

# -------------------------------
# RFM SCORING (AUTO)
# -------------------------------

def calculate_r_score(recency):
    if recency <= 30:
        return 5
    elif recency <= 60:
        return 4
    elif recency <= 90:
        return 3
    elif recency <= 120:
        return 2
    else:
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
    else:
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
    else:
        return 1


def calculate_rfm_score(row):
    r = calculate_r_score(row["Recency"])
    f = calculate_f_score(row["Total_Purchases"])
    m = calculate_m_score(row["Total_Spending"])
    return r + f + m


# -------------------------------
# RFM → Risk %
# -------------------------------

def rfm_to_risk_percentage(rfm_score):
    # Max RFM = 15
    risk_pct = (1 - (rfm_score / 15)) * 100
    return round(risk_pct, 2)


def risk_level(risk_pct):
    if risk_pct >= 70:
        return "High Risk"
    elif risk_pct >= 40:
        return "Medium Risk"
    else:
        return "Low Risk"


# -------------------------------
# Retention Strategy
# -------------------------------

def retention_action(segment, risk):

    if risk == "High Risk":
        if segment == "Loyal High-Value Customers":
            return "VIP retention, personal outreach, exclusive benefits"
        elif segment == "Deal-Driven Active Customers":
            return "Aggressive limited-time discounts & reminders"
        else:
            return "Win-back campaign or cost-controlled exit"

    elif risk == "Medium Risk":
        return "Engagement nudges, personalized recommendations"

    else:
        return "Loyalty rewards, cross-sell & upsell"


# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(page_title="Customer Retention Engine", layout="centered")
st.title("📊 Customer Segmentation & Retention App")

st.sidebar.header("Customer Input")

with st.sidebar.form("customer_form"):

    input_data = {
        "Recency": st.number_input("Recency (days since last purchase)", min_value=0),
        "Total_Spending": st.number_input("Total Spending", min_value=0.0),
        "NumWebPurchases": st.number_input("Web Purchases", min_value=0),
        "NumStorePurchases": st.number_input("Store Purchases", min_value=0),
        "NumCatalogPurchases": st.number_input("Catalog Purchases", min_value=0),
        "NumDealsPurchases": st.number_input("Deals Purchases", min_value=0),
        "NumWebVisitsMonth": st.number_input("Web Visits / Month", min_value=0),
        "Income": st.number_input("Income", min_value=10000),
        "Age": st.number_input("Age", min_value=18)
    }

    submit = st.form_submit_button("Predict")

# -------------------------------
# Prediction
# -------------------------------

if submit:

    # Frequency = total purchases
    input_data["Total_Purchases"] = (
        input_data["NumWebPurchases"]
        + input_data["NumStorePurchases"]
        + input_data["NumCatalogPurchases"]
    )

    df_input = pd.DataFrame([input_data])

    # KMeans input
    model_features = scaler.feature_names_in_
    df_model = df_input.reindex(columns=model_features)

    scaled_input = scaler.transform(df_model)
    cluster = int(kmeans.predict(scaled_input)[0])

    segment = segment_map[cluster]
    description = cluster_description[cluster]

    # RFM & Risk
    rfm_score = calculate_rfm_score(input_data)
    risk_pct = rfm_to_risk_percentage(rfm_score)
    risk = risk_level(risk_pct)

    action = retention_action(segment, risk)

    # -------------------------------
    # OUTPUT
    # -------------------------------

    st.subheader("🔍 Prediction Result")

    c1, c2, c3 = st.columns(3)
    c1.metric("Cluster", cluster)
    c2.metric("RFM Score", f"{rfm_score} / 15")
    c3.metric("Risk Percentage", f"{risk_pct}%")

    st.markdown("### ⚠️ Risk Level")
    st.success(risk)

    st.markdown("### 🧑‍💼 Customer Segment")
    st.success(segment)

    st.subheader("🧩 Cluster Description")
    st.info(description)

    st.subheader("🎯 Recommended Retention Action")
    st.success(action)

else:
    st.info("👈 Enter customer details and click Predict")
