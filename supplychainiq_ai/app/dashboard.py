from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_pipeline import load_supply_chain_data
from src.features import create_features
from src.model_service import SupplyChainService


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "supply_chain_data.csv"

st.set_page_config(page_title="SupplyChainIQ AI", page_icon="📦", layout="wide")
st.title("📦 SupplyChainIQ AI")
st.caption("Demand forecasting, stockout risk, inventory optimization, and supplier intelligence.")

if not (ROOT / "models" / "metadata.json").exists():
    st.error("Models are not trained. Run: python scripts/train_models.py")
    st.stop()

service = SupplyChainService()
raw = load_supply_chain_data(DATA)
features = create_features(raw)

with st.sidebar:
    product = st.selectbox("Product", sorted(raw["product_id"].unique()))
    store = st.selectbox("Store", sorted(raw["store_id"].unique()))
    st.subheader("Model performance")
    st.json(service.metrics)

filtered = features[
    (features["product_id"] == product) &
    (features["store_id"] == store)
].copy()

latest = filtered.iloc[-1].to_dict()
prediction = service.predict(latest)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Forecast daily demand", f"{prediction['forecast_daily_demand']:.1f}")
c2.metric("Stockout probability", f"{prediction['stockout_probability']*100:.1f}%")
c3.metric("Reorder quantity", f"{prediction['recommended_reorder_quantity']:.0f}")
c4.metric("Risk level", prediction["risk_level"])

c5, c6, c7, c8 = st.columns(4)
c5.metric("Safety stock", f"{prediction['safety_stock']:.0f}")
c6.metric("Reorder point", f"{prediction['reorder_point']:.0f}")
c7.metric("Inventory cover", f"{prediction['days_of_inventory_cover']:.1f} days")
c8.metric("Expected lost sales", f"${prediction['expected_lost_sales']:,.0f}")

st.subheader("Demand and inventory trend")
plot_data = raw[
    (raw["product_id"] == product) &
    (raw["store_id"] == store)
].tail(120)

trend = plot_data.melt(
    id_vars=["date"],
    value_vars=["demand", "closing_inventory"],
    var_name="series",
    value_name="value",
)
st.plotly_chart(
    px.line(trend, x="date", y="value", color="series"),
    use_container_width=True,
)

left, right = st.columns(2)

with left:
    st.subheader("Recommendations")
    for item in prediction["recommendations"]:
        st.write(f"• {item}")

with right:
    st.subheader("Risk indicators")
    st.write(f"Anomaly detected: **{'Yes' if prediction['anomaly_detected'] else 'No'}**")
    st.write(f"Anomaly score: **{prediction['anomaly_score']:.3f}**")
    st.write(f"Supplier risk score: **{prediction['supplier_risk_score']:.3f}**")
    st.write(f"Overstock risk: **{'Yes' if prediction['overstock_risk'] else 'No'}**")

st.subheader("Scenario simulation")
with st.form("scenario_form"):
    cols = st.columns(4)
    demand_change = cols[0].slider("Demand change %", -50, 100, 0)
    lead_change = cols[1].slider("Lead-time change %", -50, 100, 0)
    promo_uplift = cols[2].slider("Promotion uplift %", 0, 100, 0)
    transfer_qty = cols[3].number_input("Inventory transfer quantity", value=0.0)
    submitted = st.form_submit_button("Run scenario")

if submitted:
    scenario = service.scenario(
        baseline_demand=prediction["forecast_daily_demand"],
        current_inventory=float(latest["closing_inventory"]),
        demand_change_pct=demand_change,
        lead_time_change_pct=lead_change,
        promotion_uplift_pct=promo_uplift,
        transfer_quantity=transfer_qty,
    )
    st.json(scenario)

st.subheader("Regional stockout exposure")
regional = raw.groupby("region", as_index=False).agg(
    stockout_rate=("stockout_flag", "mean"),
    lost_sales=("lost_sales_value", "sum"),
)
st.plotly_chart(
    px.bar(regional, x="region", y="lost_sales", color="stockout_rate"),
    use_container_width=True,
)
