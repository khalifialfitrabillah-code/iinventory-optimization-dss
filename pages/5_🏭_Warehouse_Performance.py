import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Silakan login terlebih dahulu.")
    st.stop()

import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🏭 Warehouse Performance")
st.caption("Warehouse Monitoring Dashboard")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("data/inventory_final.csv")

# =====================================================
# AGGREGATION
# =====================================================

warehouse_summary = (
    df.groupby("Warehouse_ID")
    .agg({
        "Current_Inventory":"sum",
        "Forecast_Demand":"sum",
        "Service_Level":"mean",
        "Inventory_Turnover":"mean",
        "Stock_Ratio":"mean"
    })
    .reset_index()
)

# =====================================================
# KPI
# =====================================================

st.subheader("📊 Warehouse Summary")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Warehouse",
        warehouse_summary.shape[0]
    )

with col2:
    st.metric(
        "Avg Service Level",
        f"{warehouse_summary['Service_Level'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Avg Turnover",
        f"{warehouse_summary['Inventory_Turnover'].mean():.2f}"
    )

with col4:
    st.metric(
        "Avg Stock Ratio",
        f"{warehouse_summary['Stock_Ratio'].mean():.2f}"
    )

st.markdown("---")

# =====================================================
# INVENTORY BY WAREHOUSE
# =====================================================

st.subheader("📦 Inventory by Warehouse")

fig = px.bar(
    warehouse_summary,
    x="Warehouse_ID",
    y="Current_Inventory",
    color="Current_Inventory",
    text="Current_Inventory"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FORECAST DEMAND
# =====================================================

st.subheader("📈 Forecast Demand by Warehouse")

fig = px.bar(
    warehouse_summary,
    x="Warehouse_ID",
    y="Forecast_Demand",
    color="Forecast_Demand",
    text="Forecast_Demand"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# SERVICE LEVEL
# =====================================================

st.subheader("🎯 Service Level by Warehouse")

fig = px.bar(
    warehouse_summary,
    x="Warehouse_ID",
    y="Service_Level",
    color="Service_Level",
    text="Service_Level"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# INVENTORY TURNOVER
# =====================================================

st.subheader("🔄 Inventory Turnover")

fig = px.bar(
    warehouse_summary,
    x="Warehouse_ID",
    y="Inventory_Turnover",
    color="Inventory_Turnover",
    text="Inventory_Turnover"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# WAREHOUSE RANKING
# =====================================================

st.subheader("🏆 Warehouse Ranking")

ranking = warehouse_summary.sort_values(
    by="Service_Level",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

st.markdown("---")

st.success(
    """
    Warehouse dengan Service Level tinggi
    menunjukkan performa distribusi yang baik.

    Inventory Turnover tinggi menunjukkan
    perputaran stok yang efisien.

    Dashboard ini membantu manajemen
    mengevaluasi performa setiap gudang.
    """
)