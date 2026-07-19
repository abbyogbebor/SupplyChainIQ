from src.inventory_engine import calculate_inventory_policy, classify_inventory_risk


def test_reorder_quantity_is_positive_when_inventory_is_low():
    result = calculate_inventory_policy(
        forecast_daily_demand=20,
        demand_std=4,
        lead_time_days=10,
        current_inventory=50,
    )
    assert result["recommended_reorder_quantity"] > 0


def test_critical_risk_when_cover_is_below_lead_time():
    assert classify_inventory_risk(0.2, 3, 10) == "Critical"
