import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Silakan login terlebih dahulu.")
    st.stop()

import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Inventory Optimization DSS",
    page_icon="📦",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.hero {
    background: linear-gradient(
        135deg,
        #1e3a8a,
        #2563eb
    );
    padding: 35px;
    border-radius: 15px;
    color: white;
    margin-bottom: 25px;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv("data/inventory_final.csv")

# ==================================================
# KPI CALCULATION
# ==================================================

holding_cost = df["Holding_Cost"].sum()
ordering_cost = df["Ordering_Cost"].sum()

inventory_cost = holding_cost + ordering_cost

service_level = df["Service_Level"].mean()

stockout_sku = (df["Stockout_Risk"] == 1).sum()
overstock_sku = (df["Overstock_Risk"] == 1).sum()

# ==================================================
# HERO SECTION
# ==================================================

st.markdown("""
<div class="hero">

<h1>📦 Inventory Optimization DSS</h1>

<h3>PT Mega Retail Indonesia</h3>

<p>
Decision Support System untuk membantu
Demand Forecasting, Risk Monitoring,
Warehouse Performance, dan Inventory Optimization.
</p>

</div>
""", unsafe_allow_html=True)

# ==================================================
# EXECUTIVE SUMMARY
# ==================================================

st.subheader("📊 Executive Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Total Inventory Cost",
        f"Rp {inventory_cost/1000000:.2f} Jt"
    )

with col2:
    st.metric(
        "📦 Service Level",
        f"{service_level:.2f}%"
    )

with col3:
    st.metric(
        "⚠️ Stockout SKU",
        int(stockout_sku)
    )

st.markdown("---")

# ==================================================
# OPERATIONAL METRICS
# ==================================================

st.subheader("📈 Operational Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Holding Cost",
        f"Rp {holding_cost/1000000:.2f} Jt"
    )

with col2:
    st.metric(
        "Ordering Cost",
        f"Rp {ordering_cost/1000000:.2f} Jt"
    )

with col3:
    st.metric(
        "Overstock SKU",
        int(overstock_sku)
    )

with col4:
    st.metric(
        "Inventory Records",
        len(df)
    )

st.markdown("---")

# ==================================================
# INVENTORY OVERVIEW
# ==================================================

st.subheader("📦 Inventory Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Product",
        df["Product_ID"].nunique()
    )

with col2:
    st.metric(
        "Total Warehouse",
        df["Warehouse_ID"].nunique()
    )

with col3:
    st.metric(
        "Average Demand",
        f"{df['Demand'].mean():.0f}"
    )

with col4:
    st.metric(
        "Average Lead Time",
        f"{df['Lead_Time'].mean():.2f} Days"
    )

st.markdown("---")

# ==================================================
# BUSINESS OBJECTIVES
# ==================================================

st.subheader("🎯 Business Objectives")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("""
### 💰 Cost Optimization

Mengurangi biaya inventory melalui
pengendalian holding cost dan ordering cost.
""")

with col2:
    st.warning("""
### ⚠️ Risk Mitigation

Mengurangi risiko stockout
dan overstock inventory.
""")

with col3:
    st.info("""
### 📦 Service Improvement

Meningkatkan service level
dan kepuasan pelanggan.
""")

st.markdown("---")

# ==================================================
# BUSINESS PROBLEM
# ==================================================

st.subheader("📋 Business Problem")

st.info("""
PT Mega Retail Indonesia menghadapi tantangan dalam pengelolaan inventory
pada beberapa warehouse regional.

Permasalahan utama:

• Tingginya biaya inventory

• Risiko stockout

• Risiko overstock

• Ketidakseimbangan inventory antar warehouse

• Target service level yang harus dipenuhi

Dashboard ini digunakan sebagai
Inventory Optimization Decision Support System (DSS).
""")

st.markdown("---")

# ==================================================
# ANALYTICS MODULES
# ==================================================

st.subheader("🚀 Analytics Modules")

col1, col2 = st.columns(2)

with col1:

    st.success("""
### 📦 Inventory Analysis

• Inventory Distribution

• Stock Ratio Analysis

• Inventory Turnover

• Inventory Monitoring
""")

    st.success("""
### 📈 Demand Forecasting

• Forecast Demand

• Forecast Evaluation

• Demand Pattern Analysis

• Demand Distribution
""")

    st.success("""
### ⚠️ Risk Forecasting

• Stockout Risk

• Overstock Risk

• Risk Monitoring

• Risk Recommendation
""")

with col2:

    st.success("""
### 🏭 Warehouse Performance

• Warehouse Ranking

• Inventory Monitoring

• Service Level Analysis

• Warehouse Comparison
""")

    st.success("""
### 🎯 What If Analysis

• Scenario Simulation

• Demand Change Impact

• Lead Time Impact

• Safety Stock Impact
""")

    st.success("""
### ⚙️ Inventory Optimization

• EOQ Analysis

• Reorder Point

• Safety Stock

• DSS Recommendation
""")

st.markdown("---")

# ==================================================
# DSS WORKFLOW
# ==================================================

st.subheader("🔄 DSS Workflow")

st.info("""
Demand Analysis

⬇️

Demand Forecasting

⬇️

Risk Forecasting

⬇️

Inventory Optimization

⬇️

Decision Support Recommendation
""")

st.markdown("---")

# ==================================================
# DATASET SUMMARY
# ==================================================

st.subheader("🗂 Dataset Summary")

summary = pd.DataFrame({
    "Information": [
        "Total Records",
        "Total Variables",
        "Warehouse",
        "Products"
    ],
    "Value": [
        len(df),
        len(df.columns),
        df["Warehouse_ID"].nunique(),
        df["Product_ID"].nunique()
    ]
})

st.dataframe(
    summary,
    use_container_width=True
)

st.markdown("---")

# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">

Inventory Optimization DSS

Advanced Business Data Analytics

PT Mega Retail Indonesia

2026

</div>
""", unsafe_allow_html=True)