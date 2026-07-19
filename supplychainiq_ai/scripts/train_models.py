from pathlib import Path
import json
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_auc_score,
)
from xgboost import XGBClassifier, XGBRegressor

from src.data_pipeline import load_supply_chain_data
from src.features import create_features, get_feature_columns


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "supply_chain_data.csv"
MODEL_DIR = ROOT / "models"


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_supply_chain_data(DATA)
    frame = create_features(raw)
    features = get_feature_columns(frame)

    split_date = frame["date"].quantile(0.80)
    train = frame[frame["date"] <= split_date]
    test = frame[frame["date"] > split_date]

    X_train, X_test = train[features], test[features]
    y_demand_train, y_demand_test = train["demand"], test["demand"]
    y_stockout_train, y_stockout_test = train["stockout_flag"], test["stockout_flag"]

    demand_model = XGBRegressor(
        n_estimators=250,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=4,
    )
    demand_model.fit(X_train, y_demand_train)

    positives = max(1, int(y_stockout_train.sum()))
    negatives = max(1, len(y_stockout_train) - positives)

    stockout_model = XGBClassifier(
        n_estimators=220,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        eval_metric="logloss",
        scale_pos_weight=negatives / positives,
        random_state=42,
        n_jobs=4,
    )
    stockout_model.fit(X_train, y_stockout_train)

    anomaly_model = IsolationForest(
        n_estimators=180,
        contamination=0.03,
        random_state=42,
        n_jobs=-1,
    )
    anomaly_model.fit(X_train)

    demand_pred = demand_model.predict(X_test)
    stockout_prob = stockout_model.predict_proba(X_test)[:, 1]
    stockout_pred = (stockout_prob >= 0.5).astype(int)

    try:
        auc = roc_auc_score(y_stockout_test, stockout_prob)
    except ValueError:
        auc = 0.0

    metrics = {
        "demand_mae": round(float(mean_absolute_error(y_demand_test, demand_pred)), 3),
        "demand_rmse": round(float(mean_squared_error(y_demand_test, demand_pred) ** 0.5), 3),
        "demand_r2": round(float(r2_score(y_demand_test, demand_pred)), 4),
        "stockout_accuracy": round(float(accuracy_score(y_stockout_test, stockout_pred)), 4),
        "stockout_roc_auc": round(float(auc), 4),
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
    }

    joblib.dump(demand_model, MODEL_DIR / "demand_model.joblib")
    joblib.dump(stockout_model, MODEL_DIR / "stockout_model.joblib")
    joblib.dump(anomaly_model, MODEL_DIR / "anomaly_model.joblib")

    with open(MODEL_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump({
            "feature_columns": features,
            "metrics": metrics,
        }, f, indent=2)

    frame.to_csv(ROOT / "data" / "processed" / "feature_data.csv", index=False)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
