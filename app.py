import subprocess
import sys
import os
import zipfile

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Required packages installation
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

# ---------------- EXTRACT ZIP FILE ----------------
def extract_zip_if_needed():
    zip_file = "online_retail(1).zip"
    csv_file = "Online_Retail.csv"
    
    # If CSV file already exists
    if os.path.exists(csv_file):
        return csv_file
    
    # If ZIP file exists
    if os.path.exists(zip_file):
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Check what's inside the ZIP
                file_list = zip_ref.namelist()
                st.sidebar.write(f"Files in ZIP: {file_list}")
                
                csv_files = [f for f in file_list if f.endswith('.csv')]
                
                if csv_files:
                    # Extract first CSV file
                    csv_in_zip = csv_files[0]
                    zip_ref.extract(csv_in_zip)
                    st.sidebar.success(f"✅ Extracted: {csv_in_zip} from ZIP")
                    
                    # Rename if needed
                    if csv_in_zip != csv_file:
                        if os.path.exists(csv_file):
                            os.remove(csv_file)
                        os.rename(csv_in_zip, csv_file)
                    
                    return csv_file
                else:
                    st.error(f"❌ No CSV file found inside {zip_file}")
                    return None
        except Exception as e:
            st.error(f"❌ Error extracting ZIP: {str(e)}")
            return None
    else:
        st.warning(f"⚠️ File not found: {zip_file}")
        return None

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
    # First try to extract from ZIP
    csv_path = extract_zip_if_needed()
    
    if csv_path and os.path.exists(csv_path):
        # Load CSV file
        try:
            # Try different encodings
            try:
                df = pd.read_csv(csv_path, encoding="ISO-8859-1")
            except:
                df = pd.read_csv(csv_path, encoding="utf-8")
            
            st.sidebar.success(f"✅ Loaded data from: {csv_path}")
            return df
        except Exception as e:
            st.error(f"❌ Error loading CSV: {str(e)}")
    
    # If ZIP/CSV not found, use online dataset
    st.warning("⚠️ Using sample online dataset")
    try:
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/OnlineRetail.csv"
        df = pd.read_csv(url, encoding="ISO-8859-1")
        return df
    except:
        # Last resort: create sample data
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

# Load data
df = load_data()

# Debug info in sidebar
with st.sidebar:
    st.markdown("### 📊 File Status")
    
    # Show current directory
    st.write(f"Current directory: {os.getcwd()}")
    
    # List all files
    all_files = os.listdir('.')
    st.write(f"All files: {all_files}")
    
    if os.path.exists("online_retail(1).zip"):
        st.success("✅ ZIP file found")
        size = os.path.getsize("online_retail(1).zip") / 1024 / 1024
        st.write(f"ZIP size: {size:.2f} MB")
    else:
        st.error("❌ ZIP file not found")
    
    if os.path.exists("Online_Retail.csv"):
        st.success("✅ CSV file found")
    else:
        st.warning("⚠️ CSV file not found")
    
    st.write(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")

# Process data
if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
    df["Amount"] = df["Quantity"] * df["UnitPrice"]
else:
    # Add Amount column if needed
    df["Amount"] = 100  # Default value

# ---------------- HEADER ----------------
st.markdown("<div class='title'>📊 Retail Performance EDA Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Dark • Modern • Interactive • Portfolio Ready</div>", unsafe_allow_html=True)

# Show dataset preview
st.info(f"📁 Dataset: {len(df)} rows, {len(df.columns)} columns")
st.write("### Data Preview")
st.dataframe(df.head(), use_container_width=True)

# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Top Customers", "Country Analysis", "Trends", "Insights"])

# ---------------- FILTERS ----------------
st.sidebar.markdown("### Filters")

if "Country" in df.columns:
    countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", countries)

    if selected_country != "All":
        df_filtered = df[df["Country"] == selected_country]
    else:
        df_filtered = df
else:
    df_filtered = df

# ---------------- PAGES ----------------
if page == "Overview":
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='glass'><h3>Total Revenue</h3><h1>${df_filtered['Amount'].sum():,.0f}</h1></div>", unsafe_allow_html=True)
    
    with col2:
        if 'CustomerID' in df_filtered.columns:
            st.markdown(f"<div class='glass'><h3>Total Customers</h3><h1>{df_filtered['CustomerID'].nunique()}</h1></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='glass'><h3>Total Transactions</h3><h1>{len(df_filtered)}</h1></div>", unsafe_allow_html=True)
    
    with col3:
        if 'StockCode' in df_filtered.columns:
            st.markdown(f"<div class='glass'><h3>Total Products</h3><h1>{df_filtered['StockCode'].nunique()}</h1></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='glass'><h3>Data Points</h3><h1>{len(df_filtered)}</h1></div>", unsafe_allow_html=True)

    st.markdown("### Dataset Preview")
    st.dataframe(df_filtered.head(20), use_container_width=True)

elif page == "Top Customers":
    st.markdown("## 🏆 Top 10 Customers by Revenue")
    
    if 'CustomerID' in df_filtered.columns and 'Amount' in df_filtered.columns:
        top_customers = (
            df_filtered.groupby("CustomerID")["Amount"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        
        fig = px.bar(
            top_customers,
            x="CustomerID",
            y="Amount",
            text_auto=True,
            template="plotly_dark",
            title="Top 10 Customers"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("CustomerID or Amount column not found in data")

elif page == "Country Analysis":
    st.markdown("## 🌍 Top 5 Countries by Revenue")
    
    if 'Country' in df_filtered.columns and 'Amount' in df_filtered.columns:
        country_rev = (
            df_filtered.groupby("Country")["Amount"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        
        fig = px.pie(
            country_rev,
            names="Country",
            values="Amount",
            hole=0.45,
            template="plotly_dark",
            title="Revenue Distribution by Country"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Country or Amount column not found in data")

elif page == "Trends":
    st.markdown("## 📈 Monthly Revenue Trend")
    
    if 'InvoiceDate' in df_filtered.columns and 'Amount' in df_filtered.columns:
        try:
            df_filtered["InvoiceDate"] = pd.to_datetime(df_filtered["InvoiceDate"], errors="coerce")
            df_filtered["Month"] = df_filtered["InvoiceDate"].dt.to_period("M").astype(str)
            
            monthly_sales = df_filtered.groupby("Month")["Amount"].sum().reset_index()
            
            fig = px.line(
                monthly_sales,
                x="Month",
                y="Amount",
                markers=True,
                template="plotly_dark",
                title="Monthly Revenue Trend"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error processing dates: {str(e)}")
    else:
        st.warning("InvoiceDate or Amount column not found in data")

elif page == "Insights":
    st.markdown("## 🧠 Auto Insights")
    
    insights = []
    
    if 'Amount' in df.columns:
        total_revenue = df['Amount'].sum()
        insights.append(f"💰 **Total Revenue:** ${total_revenue:,.0f}")
    
    if 'CustomerID' in df.columns:
        total_customers = df['CustomerID'].nunique()
        insights.append(f"👥 **Total Customers:** {total_customers}")
    
    if 'Country' in df.columns:
        top_country = df.groupby('Country')['Amount'].sum().idxmax() if 'Amount' in df.columns else df['Country'].mode()[0]
        insights.append(f"🌍 **Top Country:** {top_country}")
    
    # Default insights if no data
    if not insights:
        insights = [
            "💰 **Sample data is being used**",
            "👥 **Upload your CSV for real insights**",
            "🌍 **Extract Online_Retail.csv from ZIP file**"
        ]
    
    st.markdown("""
    <div class='glass'>
    """ + "<br>".join(insights) + """
    <br><br>
    🔹 **Most revenue comes from a small group of customers** (Pareto principle)<br>
    🔹 **Some countries dominate overall sales**<br>
    🔹 **Revenue shows seasonal trends**<br>
    🔹 **Focus on high-value repeat customers** for growth
    </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🚀 Built with Streamlit | Retail Analytics Dashboard")
