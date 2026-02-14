📊 Customer Segmentation & Retention Intelligence System
🔍 Project Overview

This project builds an end-to-end customer segmentation and retention decision system using behavioral data.
Instead of relying on unreliable churn labels, it applies RFM analysis and retention risk scoring to identify at-risk customers and recommend actionable retention strategies.

The solution is explainable, business-aligned, and production-ready, deployed using Streamlit.

🎯 Business Problem

Organizations often struggle to:

Identify high-value vs low-value customers

Detect early retention risk without true churn labels

Design segment-specific retention strategies

Convert analytics insights into business actions

This project addresses these challenges using unsupervised learning + RFM-based risk modeling.

🧠 Solution Architecture
Raw Customer Data
        ↓
Data Cleaning & Feature Engineering
        ↓
Customer Segmentation (KMeans)
        ↓
RFM Analysis (Recency, Frequency, Monetary)
        ↓
Retention Risk Percentage (0–100)
        ↓
Segment × Risk Based Retention Strategy
        ↓
Streamlit Deployment

🧩 Key Components
1️⃣ Customer Segmentation

Algorithm: KMeans Clustering

Input: Behavioral & transactional features

Evaluation:

Elbow Method (WCSS)

Silhouette Score

Output: Interpretable customer segments

Identified Segments

Loyal High-Value Customers

Deal-Driven Active Customers

Low-Value Passive Customers

2️⃣ RFM Analysis

Recency: Days since last purchase

Frequency: Total number of purchases

Monetary: Total spending

Each metric is scored from 1 to 5, producing an RFM score ranging from 3 to 15.

3️⃣ Retention Risk Modeling (Explainable)

Retention risk is derived from the RFM score:

Risk % = (1 − RFM / 15) × 100


Risk Levels

Low Risk

Medium Risk

High Risk

✔ No synthetic churn labels
✔ Fully interpretable logic
✔ Business-friendly output

4️⃣ Retention Strategy Engine

Retention actions are determined using:

Customer Segment

Retention Risk Level

Segment	Risk Level	Recommended Action
Loyal High-Value	High	VIP retention & personal outreach
Deal-Driven Active	Medium	Targeted discounts & reminders
Low-Value Passive	High	Win-back or cost-controlled exit
Any Segment	Low	Loyalty rewards & upsell
5️⃣ Deployment (Streamlit)

User inputs customer behavioral data

App outputs:

Customer segment

RFM score

Retention risk percentage

Recommended retention action

Models loaded via serialized .pkl files

🛠️ Tech Stack

Python

Pandas, NumPy

Scikit-learn

KMeans Clustering

Joblib

Streamlit

📁 Project Structure
├── app.py
├── kmeans_model.pkl
├── scaler.pkl
├── data/
│   └── processed_dataset.csv
├── notebooks/
│   └── EDA_and_Modeling.ipynb
├── README.md

🚀 How to Run the Application
pip install -r requirements.txt
streamlit run app.py

💡 Why No ML Churn Prediction Model?

Dataset does not contain a true churn label

Synthetic churn labels introduce bias and overfitting

RFM-based retention risk is:

Widely used in industry

More interpretable

More actionable for business teams

This project focuses on retention intelligence, not black-box churn prediction.

📈 Use Cases

Retail & E-commerce

Loyalty Programs

CRM Analytics

Marketing Strategy

Consulting & Business Analytics

🏆 Key Takeaways

Demonstrates when NOT to use supervised ML

Strong emphasis on business logic & explainability

Industry-ready segmentation and retention framework

Fully deployable analytics application

👤 Author

Saurabh Mulik
B.Tech – Information Technology
Aspiring Data Scientist / ML Engineer
