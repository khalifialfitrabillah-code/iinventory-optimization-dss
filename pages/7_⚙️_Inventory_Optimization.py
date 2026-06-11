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

st.title("⚙️ Inventory Optimization")
st.caption("Decision Support System for Inventory Planning")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("data/inventory_final.csv")

# =====================================================
# DSS RECOMMENDATION
# =====================================================

conditions = [
    df["Current_Inventory"] < df["ROP"],

    (df["Current_Inventory"] >= df["ROP"]) &
    (df["Current_Inventory"] < df["Safety_Stock"]),

    df["Current_Inventory"] >= df["Safety_Stock"]
]

choices = [
    "Reorder Immediately",
    "Monitor Inventory",
    "Inventory Healthy"
]

df["Optimization_Status"] = np.select(
    conditions,
    choices,
    default="Inventory Healthy"
)

# =====================================================
# KPI
# =====================================================

avg_eoq = df["EOQ"].mean()
avg_rop = df["ROP"].mean()
avg_ss = df["Safety_Stock"].mean()
avg_forecast = df["Forecast_Demand"].mean()

st.subheader("📊 Optimization Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average EOQ",
        f"{avg_eoq:.0f}"
    )

with col2:
    st.metric(
        "Average ROP",
        f"{avg_rop:.0f}"
    )

with col3:
    st.metric(
        "Average Safety Stock",
        f"{avg_ss:.0f}"
    )

with col4:
    st.metric(
        "Avg Forecast Demand",
        f"{avg_forecast:.0f}"
    )

st.markdown("---")

# =====================================================
# EOQ DISTRIBUTION
# =====================================================

st.subheader("📦 EOQ Distribution")

fig = px.histogram(
    df,
    x="EOQ",
    nbins=25,
    title="Economic Order Quantity Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# ROP DISTRIBUTION
# =====================================================

st.subheader("🔄 Reorder Point Distribution")

fig = px.histogram(
    df,
    x="ROP",
    nbins=25,
    title="Reorder Point Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# SAFETY STOCK DISTRIBUTION
# =====================================================

st.subheader("🛡 Safety Stock Distribution")

fig = px.histogram(
    df,
    x="Safety_Stock",
    nbins=25,
    title="Safety Stock Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# OPTIMIZATION STATUS
# =====================================================

st.subheader("🎯 Optimization Recommendation")

status_count = (
    df["Optimization_Status"]
    .value_counts()
    .reset_index()
)

status_count.columns = [
    "Status",
    "Count"
]

fig = px.bar(
    status_count,
    x="Status",
    y="Count",
    color="Status",
    text="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# TOP EOQ
# =====================================================

st.subheader("🏆 Top 10 Products by EOQ")

top_eoq = df.nlargest(
    10,
    "EOQ"
)

fig = px.bar(
    top_eoq,
    x="Product_ID",
    y="EOQ",
    color="EOQ",
    text="EOQ"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    top_eoq[
        [
            "Product_ID",
            "EOQ",
            "Forecast_Demand"
        ]
    ],
    use_container_width=True
)

st.markdown("---")

# =====================================================
# TOP ROP
# =====================================================

st.subheader("🚀 Top 10 Products by ROP")

top_rop = df.nlargest(
    10,
    "ROP"
)

fig = px.bar(
    top_rop,
    x="Product_ID",
    y="ROP",
    color="ROP",
    text="ROP"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    top_rop[
        [
            "Product_ID",
            "ROP",
            "Current_Inventory"
        ]
    ],
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DSS TABLE
# =====================================================

st.subheader("📋 Inventory Decision Table")

st.dataframe(
    df[
        [
            "Product_ID",
            "Current_Inventory",
            "Forecast_Demand",
            "EOQ",
            "ROP",
            "Safety_Stock",
            "Optimization_Status"
        ]
    ],
    use_container_width=True
)

st.markdown("---")

# =====================================================
# BUSINESS RECOMMENDATION
# =====================================================

st.subheader("💡 DSS Recommendation")

st.success(
    """
    Reorder Immediately:
    Inventory berada di bawah Reorder Point (ROP).

    Monitor Inventory:
    Inventory mendekati Safety Stock.

    Inventory Healthy:
    Inventory masih berada pada level optimal.

    Dashboard ini membantu manajemen
    menentukan jumlah pemesanan optimal,
    titik pemesanan ulang, dan pengendalian
    risiko stockout maupun overstock.
    """
)