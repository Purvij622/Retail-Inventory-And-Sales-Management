# 🛒 Smart Retail Analytics Platform

> An end-to-end Retail Analytics and Inventory Management Platform built using **Python, SQL Server, Streamlit, and Power BI**. The system provides real-time business intelligence, inventory monitoring, customer analytics, sales forecasting, and role-based access control for retail businesses.

---

# 📌 Project Overview

Smart Retail Analytics Platform is a complete Business Intelligence solution designed to help retail organizations monitor sales performance, manage inventory, analyze customer behavior, and forecast future demand.

The platform processes the **Brazilian Olist E-Commerce Dataset (~100,000 orders)** through a multi-layer ETL pipeline and delivers actionable insights through interactive Streamlit and Power BI dashboards.

---

# ✨ Key Features

## 🔐 Authentication & Security

* Secure Login & Signup System
* Password hashing using bcrypt
* Email validation and password strength checking
* Role-Based Access Control (Admin, Analyst, Viewer)
* Secure database configuration using environment variables (.env)

---

## 📊 Executive Dashboard

* Total Revenue KPI
* Total Orders KPI
* Total Customers KPI
* Average Order Value
* Monthly Revenue Trend Analysis
* Real-Time Low Stock Alerts

---

## 📦 Inventory Management

* Inventory Monitoring Dashboard
* Product Stock Tracking
* Low Stock Detection
* Out-of-Stock Alerts
* Add New Products (Admin / Analyst)
* Inventory Value Calculation
* Stock Level Visualization

---

## 📈 Sales Forecasting

* Historical Sales Analysis
* Forecast vs Actual Comparison
* Future Revenue Prediction
* Growth Percentage Calculation
* Automated Business Recommendations

---

## 🤖 AI Business Intelligence

* Top Revenue Generating States
* Customer Segmentation Insights
* Forecast Growth Analysis
* Inventory Risk Detection
* Automated Business Recommendations

---

## 👥 Customer Segmentation

Customer classification based on purchasing behavior:

* VIP Customers
* Regular Customers
* New Customers

Features:

* Segment Distribution
* Customer Analytics Dashboard
* Customer Behavior Insights

---

## 🏆 Performance Scorecard

Business performance monitoring through:

* Revenue Score
* Inventory Score
* Forecast Score
* Customer Score
* Overall Business Health Score
* Risk Indicators

---

## 🌍 Universal Analytics Engine

Upload any CSV dataset and instantly generate:

* Dataset Summary
* Statistical Analysis
* Missing Value Analysis
* Correlation Analysis
* Data Visualization
* AI-Powered Insights

---

## ⚙️ Admin Panel

* User Management
* Role Assignment
* User Deletion
* System Administration Controls

---

## 📊 Power BI Dashboards

### Executive Dashboard

* Revenue Analysis
* Orders Analysis
* Customer Analysis
* State-wise Sales Performance
* Monthly Revenue Trends

### Forecast Dashboard

* Current Sales
* Forecast Sales
* Sales vs Forecast Comparison
* Revenue Trend Analysis

---

# 🏗️ System Architecture

```text
Raw Olist Dataset
        │
        ▼
 Bronze Layer
 (Raw Data Storage)
        │
        ▼
 Bronze → Silver ETL
 (Cleaning & Transformation)
        │
        ▼
 Silver Layer
        │
        ▼
 Silver → Gold ETL
 (Business Metrics)
        │
        ▼
 Gold Layer
        │
        ├──────────► SQL Server
        │
        ├──────────► Streamlit Dashboards
        │
        └──────────► Power BI Reports
```

---

# 🛠️ Technology Stack

| Layer                | Technology       |
| -------------------- | ---------------- |
| Frontend             | Streamlit        |
| Database             | SQL Server       |
| Programming Language | Python           |
| Data Processing      | Pandas, NumPy    |
| Security             | bcrypt           |
| Configuration        | python-dotenv    |
| Visualization        | Power BI         |
| Analytics            | Streamlit Charts |

---

# 📁 Project Structure

```text
SmartRetailProject/

├── dashboards/
│   ├── streamlit/
│   │   ├── app.py
│   │   ├── db_connection.py
│   │   └── pages/
│   │       ├── login.py
│   │       ├── signup.py
│   │       ├── dashboard.py
│   │       ├── inventory.py
│   │       ├── forecasting.py
│   │       ├── ai_insights.py
│   │       ├── customer_segmentation.py
│   │       ├── performance_scorecard.py
│   │       ├── universal_analytics.py
│   │       └── admin.py
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── notebooks/
│   ├── bronze_to_silver.py
│   ├── silver_to_gold.py
│   └── forecasting_pipeline.py
│
├── sql/
│   └── create_tables.sql
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/SmartRetailAnalyticsPlatform.git
cd SmartRetailAnalyticsPlatform
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Database

Create a `.env` file:

```env
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=SmartRetailDB
DB_TRUSTED=yes
```

## Run ETL Pipeline

```bash
python notebooks/bronze_to_silver.py

python notebooks/silver_to_gold.py

python notebooks/forecasting_pipeline.py
```

## Launch Application

```bash
cd dashboards/streamlit

streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

# 👥 User Roles

| Role    | Permissions                         |
| ------- | ----------------------------------- |
| Admin   | Full Access                         |
| Analyst | Analytics + Inventory + Forecasting |
| Viewer  | Dashboard Access Only               |

---

# 📊 Dataset

Brazilian E-Commerce Public Dataset by Olist

Dataset Size:

* ~100,000 Orders
* Customers
* Payments
* Products
* Inventory Data
* Reviews

Source:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

---



# 🔮 Future Enhancements

* Azure Databricks Integration
* Apache Airflow Scheduling
* Advanced ML Forecasting (ARIMA / Prophet)
* Automated Email Alerts
* Real-Time Streaming Analytics
* Cloud Deployment

---

# 📄 License

Developed for educational and internship purposes.

---

# 👨‍💻 Author
Purvi Jain

CSE (AI)

Smart Retail Analytics Platform
