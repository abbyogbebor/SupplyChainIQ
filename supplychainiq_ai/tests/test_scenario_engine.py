from src.scenario_engine import simulate_scenario


def test_promotion_increases_demand():
    result = simulate_scenario(
        baseline_demand=100,
        current_inventory=120,
        promotion_uplift_pct=20,
    )
    assert result["scenario_demand"] > result["baseline_demand"]


def test_transfer_increases_inventory():
    result = simulate_scenario(
        baseline_demand=100,
        current_inventory=80,
        transfer_quantity=25,
    )
    assert result["scenario_inventory"] == 105
