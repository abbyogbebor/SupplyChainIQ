from pathlib import Path
from src.data_pipeline import load_supply_chain_data


def test_dataset_loads():
    path = Path(__file__).resolve().parents[1] / "data" / "raw" / "supply_chain_data.csv"
    data = load_supply_chain_data(path)
    assert not data.empty
    assert "demand" in data.columns
    assert "stockout_flag" in data.columns
