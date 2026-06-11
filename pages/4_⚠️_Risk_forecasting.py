import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Silakan login terlebih dahulu.")
    st.stop()

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =====================================================
# PAGE TITLE
# =====================================================

st.title("⚠️ Risk Forecasting")
st.caption("Inventory Risk Monitoring & Decision Support System")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("data/inventory_final.csv")

# =====================================================
# RISK CONVERSION
# =====================================================

df["Stockout_Label"] = np.where(
    df["Stockout_Risk"] == 1,
    "High Risk",
    "Low Risk"
)

df["Overstock_Label"] = np.where(
    df["Overstock_Risk"] == 1,
    "Overstock",
    "Normal"
)

# =====================================================
# INVENTORY RECOMMENDATION
# =====================================================

conditions = [
    df["Current_Inventory"] < df["Forecast_Demand"],

    df["Current_Inventory"] >
    (df["Forecast_Demand"] * 1.5)
]

choices = [
    "Increase Inventory",
    "Reduce Inventory"
]

df["Recommendation"] = np.select(
    conditions,
    choices,
    default="Maintain Inventory"
)

# =====================================================
# KPI
# =====================================================

stockout_count = (
    df["Stockout_Risk"] == 1
).sum()

overstock_count = (
    df["Overstock_Risk"] == 1
).sum()

increase_count = (
    df["Recommendation"] ==
    "Increase Inventory"
).sum()

reduce_count = (
    df["Recommendation"] ==
    "Reduce Inventory"
).sum()

st.subheader("📊 Risk Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Stockout Risk",
        int(stockout_count)
    )

with col2:
    st.metric(
        "Overstock Risk",
        int(overstock_count)
    )

with col3:
    st.metric(
        "Increase Inventory",
        int(increase_count)
    )

with col4:
    st.metric(
        "Reduce Inventory",
        int(reduce_count)
    )

st.markdown("---")

# =====================================================
# STOCKOUT DISTRIBUTION
# =====================================================

st.subheader("🚨 Stockout Risk Distribution")

stockout_chart = (
    df["Stockout_Label"]
    .value_counts()
    .reset_index()
)

stockout_chart.columns = [
    "Risk",
    "Count"
]

fig = px.pie(
    stockout_chart,
    names="Risk",
    values="Count",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# OVERSTOCK DISTRIBUTION
# =====================================================

st.subheader("📦 Overstock Risk Distribution")

overstock_chart = (
    df["Overstock_Label"]
    .value_counts()
    .reset_index()
)

overstock_chart.columns = [
    "Status",
    "Count"
]

fig = px.pie(
    overstock_chart,
    names="Status",
    values="Count",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# RECOMMENDATION DISTRIBUTION
# =====================================================

st.subheader("🎯 Inventory Recommendation Distribution")

rec_chart = (
    df["Recommendation"]
    .value_counts()
    .reset_index()
)

rec_chart.columns = [
    "Recommendation",
    "Count"
]

fig = px.bar(
    rec_chart,
    x="Recommendation",
    y="Count",
    color="Recommendation",
    text="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# TOP STOCKOUT PRODUCTS
# =====================================================

st.subheader("🚨 Top 10 Potential Stockout Products")

top_stockout = df.sort_values(
    by="Forecast_Demand",
    ascending=False
).head(10)

st.dataframe(
    top_stockout[
        [
            "Product_ID",
            "Demand",
            "Forecast_Demand",
            "Current_Inventory"
        ]
    ],
    use_container_width=True
)

# =====================================================
# TOP OVERSTOCK PRODUCTS
# =====================================================

st.subheader("📦 Top 10 Potential Overstock Products")

top_overstock = df.sort_values(
    by="Current_Inventory",
    ascending=False
).head(10)

st.dataframe(
    top_overstock[
        [
            "Product_ID",
            "Current_Inventory",
            "Forecast_Demand"
        ]
    ],
    use_container_width=True
)

st.markdown("---")

# =====================================================
# RECOMMENDATION TABLE
# =====================================================

st.subheader("💡 DSS Recommendation Table")

st.dataframe(
    df[
        [
            "Product_ID",
            "Current_Inventory",
            "Forecast_Demand",
            "Recommendation"
        ]
    ].head(20),
    use_container_width=True
)

st.markdown("---")

st.success(
    """
    Decision Support Recommendation:

    • Increase Inventory → stok lebih rendah dari forecast demand

    • Maintain Inventory → stok masih dalam batas optimal

    • Reduce Inventory → stok terlalu tinggi dan berpotensi overstock
    """
)