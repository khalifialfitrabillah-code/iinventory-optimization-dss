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

st.title("📈 Demand Forecasting")
st.caption("Predictive Analytics Dashboard")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("data/inventory_final.csv")

# =====================================================
# FORECAST ACCURACY
# =====================================================

actual = df["Demand"]
forecast = df["Forecast_Demand"]

mae = np.mean(np.abs(actual - forecast))

mape = np.mean(
    np.abs((actual - forecast) / actual)
) * 100

rmse = np.sqrt(
    np.mean((actual - forecast) ** 2)
)

r2 = 1 - (
    np.sum((actual - forecast) ** 2)
    /
    np.sum((actual - np.mean(actual)) ** 2)
)

# =====================================================
# KPI
# =====================================================

st.subheader("🎯 Forecast Model Evaluation")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "MAE",
        f"{mae:.2f}"
    )

with col2:
    st.metric(
        "MAPE",
        f"{mape:.2f}%"
    )

with col3:
    st.metric(
        "RMSE",
        f"{rmse:.2f}"
    )

with col4:
    st.metric(
        "R² Score",
        f"{r2:.3f}"
    )

st.markdown("---")

# =====================================================
# ACTUAL VS FORECAST
# =====================================================

st.subheader("📊 Actual vs Forecast Demand")

sample_df = df.head(50)

fig = px.line(
    sample_df,
    y=[
        "Demand",
        "Forecast_Demand"
    ],
    title="Actual vs Forecast Demand"
)

fig.update_layout(
    xaxis_title="Product Index",
    yaxis_title="Demand"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DEMAND DISTRIBUTION
# =====================================================

st.subheader("📦 Demand Distribution")

fig = px.histogram(
    df,
    x="Demand",
    nbins=20,
    title="Demand Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# FORECAST DISTRIBUTION
# =====================================================

st.subheader("🔮 Forecast Demand Distribution")

fig = px.histogram(
    df,
    x="Forecast_Demand",
    nbins=20,
    title="Forecast Demand Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# FORECAST GAP
# =====================================================

st.subheader("📉 Forecast Error Analysis")

df["Forecast_Error"] = (
    df["Forecast_Demand"]
    -
    df["Demand"]
)

fig = px.histogram(
    df,
    x="Forecast_Error",
    nbins=20,
    title="Forecast Error Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# TOP FORECAST PRODUCTS
# =====================================================

st.subheader("🏆 Top 10 Forecast Demand Products")

top_forecast = df.nlargest(
    10,
    "Forecast_Demand"
)

fig = px.bar(
    top_forecast,
    x="Product_ID",
    y="Forecast_Demand",
    color="Forecast_Demand",
    text="Forecast_Demand"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    top_forecast[
        [
            "Product_ID",
            "Demand",
            "Forecast_Demand"
        ]
    ],
    use_container_width=True
)

st.markdown("---")

# =====================================================
# SUMMARY
# =====================================================

st.success(
    """
    Forecast Demand digunakan untuk
    mendukung keputusan EOQ,
    Reorder Point (ROP),
    Safety Stock,
    dan Inventory Optimization.
    """
)