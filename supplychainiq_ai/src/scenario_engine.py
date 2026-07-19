def simulate_scenario(
    baseline_demand: float,
    current_inventory: float,
    demand_change_pct: float = 0.0,
    lead_time_change_pct: float = 0.0,
    promotion_uplift_pct: float = 0.0,
    transfer_quantity: float = 0.0,
) -> dict:
    scenario_demand = baseline_demand * (1 + demand_change_pct / 100)
    scenario_demand *= (1 + promotion_uplift_pct / 100)
    scenario_inventory = current_inventory + transfer_quantity

    demand_change = scenario_demand - baseline_demand
    inventory_gap = scenario_inventory - scenario_demand

    return {
        "baseline_demand": round(baseline_demand, 2),
        "scenario_demand": round(scenario_demand, 2),
        "scenario_inventory": round(scenario_inventory, 2),
        "demand_change": round(demand_change, 2),
        "inventory_gap": round(inventory_gap, 2),
        "lead_time_change_pct": round(lead_time_change_pct, 2),
    }
