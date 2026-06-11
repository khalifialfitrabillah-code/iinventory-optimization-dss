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

st.title("🎯 What If Analysis")
st.caption("Inventory Scenario Simulation")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("data/inventory_final.csv")

# =====================================================
# USER INPUT
# =====================================================

st.subheader("⚙️ Scenario Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    demand_change = st.slider(
        "Demand Change (%)",
        -50,
        100,
        20
    )

with col2:
    leadtime_change = st.slider(
        "Lead Time Change (%)",
        -50,
        100,
        20
    )

with col3:
    safety_change = st.slider(
        "Safety Stock Change (%)",
        -50,
        100,
        10
    )

# =====================================================
# SCENARIO CALCULATION
# =====================================================

scenario_df = df.copy()

scenario_df["New_Demand"] = (
    scenario_df["Demand"]
    * (1 + demand_change / 100)
)

scenario_df["New_Lead_Time"] = (
    scenario_df["Lead_Time"]
    * (1 + leadtime_change / 100)
)

scenario_df["New_Safety_Stock"] = (
    scenario_df["Safety_Stock"]
    * (1 + safety_change / 100)
)

scenario_df["New_ROP"] = (
    scenario_df["New_Demand"]
    * scenario_df["New_Lead_Time"] / 30
) + scenario_df["New_Safety_Stock"]

# =====================================================
# KPI
# =====================================================

st.subheader("📊 Scenario Impact")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Avg Demand",
        f"{scenario_df['New_Demand'].mean():.0f}"
    )

with col2:
    st.metric(
        "Avg Lead Time",
        f"{scenario_df['New_Lead_Time'].mean():.1f}"
    )

with col3:
    st.metric(
        "Avg Safety Stock",
        f"{scenario_df['New_Safety_Stock'].mean():.0f}"
    )

with col4:
    st.metric(
        "Avg ROP",
        f"{scenario_df['New_ROP'].mean():.0f}"
    )

st.markdown("---")

# =====================================================
# DEMAND COMPARISON
# =====================================================

st.subheader("📈 Demand Comparison")

comparison = pd.DataFrame({
    "Metric":[
        "Current Demand",
        "Scenario Demand"
    ],
    "Value":[
        df["Demand"].mean(),
        scenario_df["New_Demand"].mean()
    ]
})

fig = px.bar(
    comparison,
    x="Metric",
    y="Value",
    color="Metric",
    text="Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# SAFETY STOCK COMPARISON
# =====================================================

st.subheader("🛡 Safety Stock Comparison")

comparison_ss = pd.DataFrame({
    "Metric":[
        "Current",
        "Scenario"
    ],
    "Value":[
        df["Safety_Stock"].mean(),
        scenario_df["New_Safety_Stock"].mean()
    ]
})

fig = px.bar(
    comparison_ss,
    x="Metric",
    y="Value",
    color="Metric",
    text="Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# ROP COMPARISON
# =====================================================

st.subheader("🔄 Reorder Point Comparison")

comparison_rop = pd.DataFrame({
    "Metric":[
        "Current ROP",
        "Scenario ROP"
    ],
    "Value":[
        df["ROP"].mean(),
        scenario_df["New_ROP"].mean()
    ]
})

fig = px.bar(
    comparison_rop,
    x="Metric",
    y="Value",
    color="Metric",
    text="Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP IMPACT PRODUCTS
# =====================================================

st.subheader("🚨 Top 10 Impacted Products")

scenario_df["ROP_Change"] = (
    scenario_df["New_ROP"]
    - scenario_df["ROP"]
)

top_impact = scenario_df.nlargest(
    10,
    "ROP_Change"
)

st.dataframe(
    top_impact[
        [
            "Product_ID",
            "Demand",
            "ROP",
            "New_ROP",
            "ROP_Change"
        ]
    ],
    use_container_width=True
)

st.markdown("---")

st.success(
    """
    What-If Analysis membantu manajemen
    mengevaluasi dampak perubahan demand,
    lead time, dan safety stock terhadap
    kebutuhan persediaan di masa depan.
    """
)