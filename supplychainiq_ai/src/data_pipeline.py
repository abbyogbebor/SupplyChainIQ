from pathlib import Path
import pandas as pd


def load_supply_chain_data(path: str | Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    required = {
        "date", "product_id", "store_id", "supplier_id", "demand",
        "closing_inventory", "supplier_lead_time_days",
        "supplier_reliability", "stockout_flag"
    }
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"])
    return data.sort_values(["product_id", "store_id", "date"]).reset_index(drop=True)
