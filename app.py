import streamlit as st
import pandas as pd
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
    try:
        # Try to read from ZIP
        df = pd.read_csv("Online_Retail (1).zip", encoding="ISO-8859-1", compression='zip')
    except:
        try:
            # Try to read from CSV
            df = pd.read_csv("Online_Retail (1).csv", encoding="ISO-

df = load_data()
df["Amount"] = df["Quantity"] * df["UnitPrice"]

# ---------------- HEADER ----------------
st.markdown("<div class='title'>📊 Retail Performance EDA Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Dark • Modern • Interactive • Portfolio Ready</div>", unsafe_allow_html=True)
st.markdown("")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Top Customers", "Country Analysis", "Trends", "Insights"])

# ---------------- FILTERS ----------------
st.sidebar.markdown("### Filters")

if "Country" in df.columns:
    countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", countries)

    if selected_country != "All":
        df = df[df["Country"] == selected_country]

# ---------------- OVERVIEW ----------------
if page == "Overview":
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='glass'><h3>Total Revenue</h3><h1>${df['Amount'].sum():,.0f}</h1></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='glass'><h3>Total Customers</h3><h1>{df['CustomerID'].nunique()}</h1></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='glass'><h3>Total Products</h3><h1>{df['StockCode'].nunique()}</h1></div>", unsafe_allow_html=True)

    st.markdown("### Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)

# ---------------- TOP CUSTOMERS ----------------
elif page == "Top Customers":
    st.markdown("## 🏆 Top 10 Customers by Revenue")

    top_customers = (
        df.groupby("CustomerID")["Amount"]
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
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- COUNTRY ANALYSIS ----------------
elif page == "Country Analysis":
    st.markdown("## 🌍 Top 5 Countries by Revenue")

    country_rev = (
        df.groupby("Country")["Amount"]
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
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- TRENDS ----------------
elif page == "Trends":
    st.markdown("## 📈 Monthly Revenue Trend")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    monthly_sales = df.groupby("Month")["Amount"].sum().reset_index()

    fig = px.line(
        monthly_sales,
        x="Month",
        y="Amount",
        markers=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- INSIGHTS ----------------
elif page == "Insights":
    st.markdown("## 🧠 Auto Insights")

    st.markdown("""
    <div class='glass'>
    🔹 Most revenue comes from a small group of customers (Pareto principle).  
    🔹 Some countries dominate overall sales.  
    🔹 Revenue shows seasonal trends.  
    🔹 Business should focus on high-value repeat customers.
    </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🚀 Built with Streamlit | Faddy KJ Dark EDA Dashboard")

