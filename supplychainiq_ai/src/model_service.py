from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd

from src.inventory_engine import calculate_inventory_policy, classify_inventory_risk
from src.recommendations import generate_recommendations
from src.scenario_engine import simulate_scenario


MODEL_DIR = Path(__file__).resolve().parents[1] / "models"


class SupplyChainService:
    def __init__(self, model_dir: Path = MODEL_DIR):
        self.demand_model = joblib.load(model_dir / "demand_model.joblib")
        self.stockout_model = joblib.load(model_dir / "stockout_model.joblib")
        self.anomaly_model = joblib.load(model_dir / "anomaly_model.joblib")
        with open(model_dir / "metadata.json", "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        self.feature_columns = self.metadata["feature_columns"]
        self.metrics = self.metadata["metrics"]

    def predict(self, feature_row: dict) -> dict:
        X = pd.DataFrame([{
            col: float(feature_row.get(col, 0.0))
            for col in self.feature_columns
        }])

        forecast_demand = max(0.0, float(self.demand_model.predict(X)[0]))
        stockout_probability = float(self.stockout_model.predict_proba(X)[0, 1])
        anomaly_raw = float(self.anomaly_model.decision_function(X)[0])
        anomaly_detected = int(self.anomaly_model.predict(X)[0]) == -1
        anomaly_score = float(np.clip(0.5 - anomaly_raw, 0, 1))

        demand_std = float(feature_row.get("demand_roll_std_30", 0.0))
        lead_time = float(feature_row.get("supplier_lead_time_days", 7.0))
        current_inventory = float(feature_row.get("closing_inventory", 0.0))

        policy = calculate_inventory_policy(
            forecast_daily_demand=forecast_demand,
            demand_std=demand_std,
            lead_time_days=lead_time,
            current_inventory=current_inventory,
        )

        risk_level = classify_inventory_risk(
            stockout_probability,
            policy["days_of_inventory_cover"],
            lead_time,
        )

        overstock_risk = policy["days_of_inventory_cover"] > 60
        supplier_risk = float(feature_row.get("supplier_risk", 0.0))
        transfer_available = bool(feature_row.get("transfer_available", 0))

        recommendations = generate_recommendations(
            risk_level,
            supplier_risk,
            overstock_risk,
            transfer_available,
        )

        selling_price = float(feature_row.get("selling_price", 0.0))
        expected_lost_sales = max(
            0.0,
            forecast_demand * lead_time - current_inventory
        ) * selling_price

        return {
            "forecast_daily_demand": round(forecast_demand, 2),
            "stockout_probability": round(stockout_probability, 4),
            "anomaly_detected": anomaly_detected,
            "anomaly_score": round(anomaly_score, 4),
            "risk_level": risk_level,
            "supplier_risk_score": round(supplier_risk, 4),
            "overstock_risk": overstock_risk,
            "expected_lost_sales": round(expected_lost_sales, 2),
            **policy,
            "recommendations": recommendations,
        }

    def scenario(self, **kwargs) -> dict:
        return simulate_scenario(**kwargs)
