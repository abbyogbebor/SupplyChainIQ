# SupplyChainIQ AI

SupplyChainIQ AI is an end-to-end demand forecasting and inventory optimization platform for retail and industrial supply chains.

The platform forecasts product demand, estimates stockout risk, calculates safety stock and reorder points, detects unusual demand patterns, scores supplier risk, recommends inventory transfers, and simulates operational scenarios.

## Main capabilities

- Product, store, and regional demand forecasting
- Time-series lag and rolling-window features
- Stockout probability estimation
- Safety-stock calculation
- Dynamic reorder-point calculation
- Recommended reorder quantity
- Overstock-risk detection
- Supplier lead-time and reliability scoring
- Demand anomaly detection
- Inventory-transfer recommendations
- Expected lost-sales estimation
- Scenario simulation
- FastAPI backend
- Streamlit dashboard
- Automated tests
- Docker support

## Technology stack

- Python
- pandas and NumPy
- scikit-learn
- XGBoost
- FastAPI
- Streamlit
- Plotly
- Joblib
- Docker

## Quick start

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Train the models:

```bash
python scripts/train_models.py
```

Run the API:

```bash
uvicorn app.api:app --reload --port 8000
```

Run the dashboard in another terminal:

```bash
streamlit run app/dashboard.py
```

Open:

- Dashboard: http://localhost:8501
- API documentation: http://localhost:8000/docs

## Important note

The included dataset is synthetic and intended for learning, demonstration, GitHub, and LinkedIn portfolio use. Real operational deployment requires validation with company-specific demand, inventory, supplier, and cost data.
