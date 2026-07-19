# Architecture

## Data layer
Daily product, store, supplier, demand, inventory, promotion, lead-time, and cost records.

## Feature layer
Calendar variables, lagged demand, rolling averages, rolling volatility, inventory cover, and supplier-risk features.

## Model layer
- XGBoost regression for demand forecasting
- XGBoost classification for stockout prediction
- Isolation Forest for anomaly detection
- Formula-based safety stock and reorder optimization
- Rule-based maintenance and transfer recommendations

## Serving layer
FastAPI serves predictions and Streamlit provides an interactive dashboard.

## Production extensions
Add ERP integration, supplier APIs, Kafka or event-stream ingestion, authentication, alerting, optimization solvers, and scheduled retraining.
