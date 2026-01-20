import subprocess
import sys
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Required packages install karein
required_packages = ['streamlit', 'pandas', 'plotly', 'numpy']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Retail Performance EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #0f172a, #020617);
    color: white;
}
.glass {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 0 30px rgba(0,0,0,0.4);
}
.title {
    font-size: 40px;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    # Try multiple file locations and names
    file_options = [
        "Online_Retail (1).csv",
        "Online_Retail.csv",
        "data/Online_Retail (1).csv",
        "OnlineRetail.csv",
        "online_retail.csv"
    ]
    
    for file_path in file_options:
        if os.path.exists(file_path):
            st.success(f"✅ Loaded data from: {file_path}")
            return pd.read_csv(file_path, encoding="ISO-8859-1")
    
    # If no local file found, use online dataset
    st.warning("⚠️ Local CSV not found. Using sample online dataset.")
    try:
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/OnlineRetail.csv"
        return pd.read_csv(url, encoding="ISO-8859-1")
    except:
        # Create dummy data as last resort
        st.info("📊 Generating sample data for demonstration...")
        np.random.seed(42)
        data = {
            'CustomerID': np.random.randint(1000, 9999, 500),
            'Quantity': np.random.randint(1, 50, 500),
            'UnitPrice': np.random.uniform(1, 1000, 500),
            'Country': np.random.choice(['UK', 'USA', 'Germany', 'France', 'India', 'Australia'], 500),
            'StockCode': [f"SKU{str(i).zfill(5)}" for i in range(500)],
            'InvoiceDate': pd.date_range('2023-01-01', periods=500, freq='D'),
            'Description': [f"Product {i}" for i in range(500)]
        }
        return pd.DataFrame(data)

df = load_data()

# Process data
if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
    df["Amount"] = df["Quantity"] * df["UnitPrice"]

# ---------------- HEADER ----------------
st.markdown("<div class='title'>📊 Retail Performance EDA Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Dark • Modern • Interactive • Portfolio Ready</div>", unsafe_allow_html=True)

# Show dataset info
st.info(f"📁 Dataset: {len(df)} rows, {len(df.columns)} columns")

# Rest of your code remains same...
# [Your existing code from sidebar onwards]
