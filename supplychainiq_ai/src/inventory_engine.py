import math


def calculate_inventory_policy(
    forecast_daily_demand: float,
    demand_std: float,
    lead_time_days: float,
    current_inventory: float,
    service_level_z: float = 1.65,
    review_period_days: int = 30,
) -> dict:
    forecast_daily_demand = max(0.0, forecast_daily_demand)
    demand_std = max(0.0, demand_std)
    lead_time_days = max(1.0, lead_time_days)

    safety_stock = service_level_z * demand_std * math.sqrt(lead_time_days)
    reorder_point = forecast_daily_demand * lead_time_days + safety_stock
    target_stock = forecast_daily_demand * (lead_time_days + review_period_days) + safety_stock
    reorder_quantity = max(0.0, target_stock - current_inventory)

    days_of_cover = (
        current_inventory / forecast_daily_demand
        if forecast_daily_demand > 0
        else float("inf")
    )

    return {
        "safety_stock": round(safety_stock, 2),
        "reorder_point": round(reorder_point, 2),
        "recommended_reorder_quantity": round(reorder_quantity, 2),
        "days_of_inventory_cover": round(days_of_cover, 2) if days_of_cover != float("inf") else 9999,
    }


def classify_inventory_risk(
    stockout_probability: float,
    days_of_cover: float,
    lead_time_days: float,
) -> str:
    if stockout_probability >= 0.75 or days_of_cover < lead_time_days:
        return "Critical"
    if stockout_probability >= 0.50 or days_of_cover < lead_time_days * 1.5:
        return "High"
    if stockout_probability >= 0.25:
        return "Medium"
    return "Low"
