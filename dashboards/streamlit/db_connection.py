# =============================================
# db_connection.py
# Path: dashboards/streamlit/db_connection.py
# =============================================

import pyodbc
import streamlit as st
from dotenv import load_dotenv
import os

# Load .env file from project root
# go up 2 levels: streamlit → dashboards → SmartRetailProject
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

def get_connection():
    """
    Reads DB credentials from .env file — NOT hardcoded.
    Returns a fresh pyodbc connection every time.
    """
    try:
        server  = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
        db_name = os.getenv("DB_NAME",   "SmartRetailDB")

        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={db_name};"
            f"Trusted_Connection=yes;"
        )
        return conn

    except pyodbc.Error as e:
        st.error(f"❌ Database connection failed: {e}")
        st.stop()