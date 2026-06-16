import streamlit as st
import pandas as pd
import requests

# -------------------------------
# CONFIG
# -------------------------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Customer Retention Engine", layout="centered")

st.title("📊 Customer Segmentation & Retention System")


# -------------------------------
# SINGLE CUSTOMER INPUT
# -------------------------------
st.sidebar.header("Single Customer Prediction")

with st.sidebar.form("single_form"):

    input_data = {
        "Recency": st.number_input("Recency (days)", min_value=0),
        "Total_Spending": st.number_input("Total Spending", min_value=0.0),
        "NumWebPurchases": st.number_input("Web Purchases", min_value=0),
        "NumStorePurchases": st.number_input("Store Purchases", min_value=0),
        "NumCatalogPurchases": st.number_input("Catalog Purchases", min_value=0),
        "NumDealsPurchases": st.number_input("Deals Purchases", min_value=0),
        "NumWebVisitsMonth": st.number_input("Web Visits/Month", min_value=0),
        "Income": st.number_input("Income", min_value=10000),
        "Age": st.number_input("Age", min_value=18)
    }

    submit = st.form_submit_button("Predict Customer")


# if submit:

#     response = requests.post(
#         f"{API_URL}/predict",
#         json=input_data
#     )

#     result = response.json()

#     st.subheader("🔍 Single Customer Result")

#     st.json(result)


if submit:

    response = requests.post(
        f"{API_URL}/predict",
        json=input_data
    )

    result = response.json()

    st.subheader("🔍 Customer Analysis Result")

    # -------------------------------
    # TOP METRICS CARDS
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Cluster", result["cluster"])
    col2.metric("RFM Score", result["rfm_score"])
    col3.metric("Risk %", f"{result['risk_percentage']}%")


    # -------------------------------
    # SEGMENT + RISK HIGHLIGHT BOX
    # -------------------------------
    st.markdown("### 🧑‍💼 Customer Segment")

    st.success(f"Segment: {result['segment']}")

    st.markdown("### ⚠️ Risk Level")

    if result["risk_level"] == "High Risk":
        st.error(f"🔥 {result['risk_level']}")
    elif result["risk_level"] == "Medium Risk":
        st.warning(f"⚠️ {result['risk_level']}")
    else:
        st.success(f"🟢 {result['risk_level']}")


    # -------------------------------
    # RECOMMENDATION BOX
    # -------------------------------
    st.markdown("### 🎯 Retention Strategy")

    st.info(result["recommendation"])


    # -------------------------------
    # DESCRIPTION BOX
    # -------------------------------
    st.markdown("### 🧩 Cluster Insight")

    st.write(result["description"])
    
# -------------------------------
# BATCH UPLOAD
# -------------------------------
st.markdown("---")
st.header("📂 Batch Prediction (CSV Upload)")

uploaded_file = st.file_uploader("Upload Customer CSV", type=["csv"])


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df.head())


    # -------------------------------
    # CALL FASTAPI BATCH ENDPOINT
    # -------------------------------
    payload = {"data": df.to_dict(orient="records")}

    response = requests.post(
        f"{API_URL}/batch_predict",
        json=payload
    )

    result_df = pd.DataFrame(response.json())


    # -------------------------------
    # RESULTS TABLE
    # -------------------------------
    st.subheader("🔮 Prediction Results")
    st.dataframe(result_df)


    # -------------------------------
    # ANALYTICS (STREAMLIT SIDE)
    # -------------------------------

    total = len(result_df)

    high_risk = len(result_df[result_df["risk_level"] == "High Risk"])
    medium_risk = len(result_df[result_df["risk_level"] == "Medium Risk"])
    low_risk = len(result_df[result_df["risk_level"] == "Low Risk"])


    st.subheader("📊 Risk Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total)
    col2.metric("🔥 High Risk", high_risk)
    col3.metric("⚠️ Medium Risk", medium_risk)
    col4.metric("🟢 Low Risk", low_risk)


    # -------------------------------
    # VISUALIZATION
    # -------------------------------

    st.subheader("📈 Risk Distribution")

    chart_data = pd.DataFrame({
        "Risk Level": ["High", "Medium", "Low"],
        "Count": [high_risk, medium_risk, low_risk]
    })

    st.bar_chart(chart_data.set_index("Risk Level"))


    # -------------------------------
    # SEGMENT ANALYSIS (optional but powerful)
    # -------------------------------

    st.subheader("🧩 Segment Distribution")

    segment_counts = result_df["segment"].value_counts()

    st.bar_chart(segment_counts)


    # -------------------------------
    # DOWNLOAD RESULTS
    # -------------------------------

    csv = result_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Predictions",
        csv,
        "customer_predictions.csv",
        "text/csv"
    )


else:
    st.info("👈 Upload a CSV file to run batch predictions")