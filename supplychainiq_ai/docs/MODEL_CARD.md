# Model Card

## Intended use
Portfolio demonstration of demand forecasting and inventory optimization.

## Models
- XGBoost demand regressor
- XGBoost stockout classifier
- Isolation Forest anomaly detector

## Inputs
Demand history, inventory, price, promotion, supplier lead time, supplier reliability, returns, weather index, and calendar features.

## Limitations
- Synthetic data
- Simplified inventory assumptions
- Does not include all operational constraints
- Must be retrained and validated on real company data
