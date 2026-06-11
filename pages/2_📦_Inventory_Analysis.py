import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Silakan login terlebih dahulu.")
    st.stop()

import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# LOAD DATA
# ==================================

df = pd.read_csv("data/inventory_final.csv")

st.title("📦 Inventory Analysis Dashboard")

st.markdown("""
Analisis kondisi inventori berdasarkan warehouse,
inventory turnover, stock ratio, dan safety stock.
""")

# ==================================
# KPI
# ==================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Inventory",
    f"{df['Current_Inventory'].sum():,.0f}"
)

col2.metric(
    "Average Stock Ratio",
    f"{df['Stock_Ratio'].mean():.2f}"
)

col3.metric(
    "Average Safety Stock",
    f"{df['Safety_Stock'].mean():.0f}"
)

col4.metric(
    "Average Inventory Turnover",
    f"{df['Inventory_Turnover'].mean():.2f}"
)

st.markdown("---")

# ==================================
# INVENTORY PER WAREHOUSE
# ==================================

st.subheader("🏭 Inventory per Warehouse")

warehouse_inventory = (
    df.groupby("Warehouse_ID")["Current_Inventory"]
    .sum()
    .reset_index()
)

fig = px.bar(
    warehouse_inventory,
    x="Warehouse_ID",
    y="Current_Inventory",
    color="Current_Inventory",
    title="Inventory per Warehouse"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================
# INVENTORY DISTRIBUTION
# ==================================

st.subheader("📊 Inventory Distribution")

fig = px.histogram(
    df,
    x="Current_Inventory",
    nbins=20,
    title="Current Inventory Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================
# STOCK RATIO ANALYSIS
# ==================================

st.subheader("📈 Stock Ratio Analysis")

fig = px.histogram(
    df,
    x="Stock_Ratio",
    nbins=20,
    title="Stock Ratio Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================
# INVENTORY TURNOVER ANALYSIS
# ==================================

st.subheader("🔄 Inventory Turnover Analysis")

fig = px.histogram(
    df,
    x="Inventory_Turnover",
    nbins=20,
    title="Inventory Turnover Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================
# SAFETY STOCK ANALYSIS
# ==================================

st.subheader("🛡️ Safety Stock Analysis")

fig = px.box(
    df,
    y="Safety_Stock",
    title="Safety Stock Spread"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================
# TOP INVENTORY TURNOVER
# ==================================

st.subheader("🏆 Top 10 Inventory Turnover")

top_turnover = (
    df.nlargest(10, "Inventory_Turnover")
      .sort_values("Inventory_Turnover")
)

fig = px.bar(
    top_turnover,
    x="Inventory_Turnover",
    y=top_turnover["Product_ID"].astype(str),
    orientation="h",
    color="Inventory_Turnover",
    text="Inventory_Turnover"
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

# ==================================
# DATA PREVIEW
# ==================================

st.subheader("📋 Inventory Dataset")

st.dataframe(df.head(20), use_container_width=True)