import pandas as pd


def create_features(data: pd.DataFrame) -> pd.DataFrame:
    frame = data.copy().sort_values(["product_id", "store_id", "date"])
    frame["year"] = frame["date"].dt.year
    frame["month"] = frame["date"].dt.month
    frame["quarter"] = frame["date"].dt.quarter
    frame["day_of_week"] = frame["date"].dt.dayofweek
    frame["day_of_year"] = frame["date"].dt.dayofyear

    grouped = frame.groupby(["product_id", "store_id"], group_keys=False)

    for lag in [1, 7, 14, 30]:
        frame[f"demand_lag_{lag}"] = grouped["demand"].shift(lag)

    for window in [7, 14, 30]:
        frame[f"demand_roll_mean_{window}"] = grouped["demand"].transform(
            lambda s: s.shift(1).rolling(window).mean()
        )
        frame[f"demand_roll_std_{window}"] = grouped["demand"].transform(
            lambda s: s.shift(1).rolling(window).std()
        )

    frame["inventory_cover_days"] = (
        frame["closing_inventory"] /
        frame["demand_roll_mean_7"].clip(lower=1)
    )
    frame["supplier_risk"] = (
        (1 - frame["supplier_reliability"]) * 0.7 +
        frame["supplier_delay_flag"] * 0.3
    )
    return frame.dropna().reset_index(drop=True)


def get_feature_columns(frame: pd.DataFrame) -> list[str]:
    excluded = {
        "date", "product_id", "product_name", "product_category",
        "store_id", "city", "region", "supplier_id", "demand",
        "stockout_flag", "reorder_quantity", "reorder_point",
        "lost_sales_value", "revenue"
    }
    return [
        c for c in frame.columns
        if c not in excluded and pd.api.types.is_numeric_dtype(frame[c])
    ]
