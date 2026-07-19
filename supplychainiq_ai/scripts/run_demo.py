from src.model_service import SupplyChainService


service = SupplyChainService()
sample = {col: 0.0 for col in service.feature_columns}
sample.update({
    "units_sold": 35,
    "opening_inventory": 75,
    "closing_inventory": 40,
    "unit_cost": 85,
    "selling_price": 145,
    "supplier_lead_time_days": 12,
    "supplier_reliability": 0.88,
    "promotion_flag": 1,
    "holiday_flag": 0,
    "weather_index": 0.2,
    "supplier_delay_flag": 1,
    "returned_units": 1,
    "holding_cost": 2.72,
    "demand_lag_1": 38,
    "demand_lag_7": 32,
    "demand_lag_14": 30,
    "demand_lag_30": 28,
    "demand_roll_mean_7": 34,
    "demand_roll_std_7": 5,
    "demand_roll_mean_14": 31,
    "demand_roll_std_14": 6,
    "demand_roll_mean_30": 29,
    "demand_roll_std_30": 7,
    "inventory_cover_days": 1.18,
    "supplier_risk": 0.42,
    "year": 2026,
    "month": 7,
    "quarter": 3,
    "day_of_week": 2,
    "day_of_year": 200,
})
print(service.predict(sample))
