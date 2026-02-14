# 📊 Customer Segmentation & Retention Intelligence System
# 🔍 Project Overview
This project builds an end-to-end customer segmentation and retention decision system using behavioral data. Instead of relying on unreliable churn labels, it applies RFM analysis and retention risk scoring to identify at-risk customers and recommend actionable retention strategies.
The solution is explainable, business-aligned, and production-ready, deployed using Streamlit.

# 🎯 Business Problem
Organizations often struggle to:
Identify high-value vs low-value customers.

Detect early retention risk without true churn labels.

Design segment-specific retention strategies.

Convert analytics insights into business actions.

This project addresses these challenges using unsupervised learning combined with RFM-based risk modeling.

# Solution Architecture
Customer Data
   ↓
Feature Engineering
   ↓
KMeans Segmentation
   ↓
RFM Scoring (3–15)
   ↓
Retention Risk % (0–100)
   ↓
Segment-Based Action
   ↓
Streamlit App
# 🧩 Key Features

Customer Segmentation using KMeans

RFM Analysis (Recency, Frequency, Monetary)

Explainable Retention Risk Percentage

Segment × Risk based Retention Strategy

Fully deployed Streamlit Dashboard

# 👥 Customer Segments

Loyal High-Value Customers

Deal-Driven Active Customers

Low-Value Passive Customers

# 🛠️ Tech Stack

Python

Pandas, NumPy

Scikit-learn

Streamlit

# 🚀 Run the App
pip install -r requirements.txt
streamlit run app.py

# Check Live 
https://customersegmentationandretentionanalysis-fy3wskj4wjm9cxesjhzqz.streamlit.app/

# 💡 Why No ML Churn Model?

No true churn label in dataset

Synthetic churn causes bias

RFM-based risk is industry-standard, interpretable, and actionable

# 📈 Use Cases

Retail & E-commerce

CRM & Marketing Analytics

Business & Consulting Analytics
