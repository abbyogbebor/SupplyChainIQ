# SupplyChainIQ AI

## AI-Powered Demand Forecasting and Inventory Optimization Platform

SupplyChainIQ AI is an end-to-end machine learning platform designed to help businesses forecast product demand, reduce stockouts, manage inventory efficiently, assess supplier risk, and improve supply-chain decision-making.

The platform combines demand forecasting, stockout prediction, anomaly detection, supplier-risk analysis, inventory optimization, scenario simulation, and an interactive dashboard in one complete solution.

---

## Project Overview

Many businesses experience supply-chain problems such as:

* Product stockouts
* Excess inventory
* Delayed supplier deliveries
* Poor demand planning
* High inventory holding costs
* Lost sales
* Overstocking
* Inefficient reorder decisions

SupplyChainIQ AI addresses these challenges by using machine learning and inventory-planning techniques to predict future demand and recommend appropriate inventory actions.

The system answers questions such as:

* How much demand should be expected for each product?
* Which products are at risk of going out of stock?
* How much safety stock should be maintained?
* When should inventory be reordered?
* How much inventory should be ordered?
* Which suppliers present the greatest operational risk?
* Which locations have excess stock that can be transferred?
* How much revenue may be lost because of stock shortages?
* What happens if demand, supplier lead time, or promotion activity changes?

---

## Key Features

### Demand Forecasting

The platform predicts future product demand using historical sales, promotions, seasonality, weather indicators, supplier information, and inventory data.

Forecasts can be generated at:

* Product level
* Store level
* Regional level
* Daily level

### Stockout Risk Prediction

A classification model estimates the probability that a product will go out of stock.

The system categorizes stockout risk as:

* Low
* Medium
* High
* Critical

### Safety Stock Calculation

The platform calculates the recommended safety-stock level using:

* Forecasted demand
* Demand variability
* Supplier lead time
* Service-level assumptions

### Dynamic Reorder Point

The system calculates the inventory level at which a new order should be placed.

The reorder point accounts for:

* Expected demand during lead time
* Demand uncertainty
* Supplier lead time
* Safety stock

### Recommended Reorder Quantity

The platform estimates how many units should be reordered based on:

* Current inventory
* Forecasted demand
* Lead time
* Review period
* Target stock level

### Supplier Risk Analysis

Suppliers are evaluated using:

* Lead-time performance
* Delivery delays
* Supplier reliability
* Historical fulfillment performance

### Demand Anomaly Detection

Isolation Forest is used to detect unusual demand and inventory patterns.

Examples include:

* Unexpected demand spikes
* Sudden demand drops
* Abnormal inventory changes
* Unusual supplier delays
* Irregular stockout patterns

### Overstock Detection

The platform identifies products with excessive inventory relative to expected future demand.

### Inventory Transfer Recommendations

The system can recommend transferring stock from overstocked locations to locations with higher demand or stockout risk.

### Expected Lost Sales

The platform estimates the potential revenue loss caused by insufficient inventory.

### Scenario Simulation

Users can test different business scenarios, including:

* Increased product demand
* Reduced demand
* Supplier delays
* Longer lead times
* Promotional campaigns
* Inventory transfers
* Demand surges
* Changes in stock availability

### Automated Recommendations

The recommendation engine generates actions such as:

* Place an urgent purchase order
* Increase monitoring frequency
* Transfer inventory between locations
* Reduce future purchase quantities
* Engage a backup supplier
* Expedite supplier delivery
* Maintain the current replenishment schedule

---

## Machine Learning Models

### XGBoost Regressor

Used for product-demand forecasting.

The model predicts future demand using:

* Historical demand
* Demand lags
* Rolling averages
* Rolling standard deviations
* Promotions
* Holidays
* Weather indicators
* Supplier information
* Inventory levels
* Calendar features

### XGBoost Classifier

Used to predict stockout probability.

### Isolation Forest

Used for anomaly detection across demand, supplier, and inventory variables.

### Inventory Optimization Engine

Formula-based inventory calculations are used for:

* Safety stock
* Reorder points
* Reorder quantities
* Inventory-cover days
* Stockout-risk classification

---

## Technology Stack

* Python
* pandas
* NumPy
* scikit-learn
* XGBoost
* FastAPI
* Streamlit
* Plotly
* Joblib
* Pydantic
* Pytest
* Docker
* Docker Compose

---

## Dataset

The project includes a synthetic supply-chain dataset containing more than 26,000 records.

The dataset includes:

* Date
* Product ID
* Product name
* Product category
* Store ID
* City
* Region
* Supplier ID
* Units sold
* Product demand
* Opening inventory
* Closing inventory
* Unit cost
* Selling price
* Supplier lead time
* Supplier reliability
* Reorder point
* Reorder quantity
* Promotion indicator
* Holiday indicator
* Weather index
* Stockout indicator
* Supplier-delay indicator
* Returned units
* Inventory holding cost
* Revenue
* Lost-sales value

The dataset is located at:

```text
data/raw/supply_chain_data.csv
```

---

## Project Structure

```text
SupplyChainIQ/
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   └── dashboard.py
│
├── src/
│   ├── __init__.py
│   ├── data_pipeline.py
│   ├── features.py
│   ├── inventory_engine.py
│   ├── model_service.py
│   ├── recommendations.py
│   └── scenario_engine.py
│
├── scripts/
│   ├── train_models.py
│   └── run_demo.py
│
├── data/
│   ├── raw/
│   │   └── supply_chain_data.csv
│   └── processed/
│
├── models/
│   └── README.md
│
├── tests/
│   ├── test_data_pipeline.py
│   ├── test_inventory_engine.py
│   └── test_scenario_engine.py
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── MODEL_CARD.md
│   └── GITHUB_UPLOAD_GUIDE.md
│
├── assets/
├── notebooks/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/abbyogbebor/SupplyChainIQ.git
```

Move into the project folder:

```bash
cd SupplyChainIQ
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

---

## Train the Models

Run:

```bash
python scripts/train_models.py
```

This command trains:

* Demand forecasting model
* Stockout prediction model
* Anomaly detection model

It also generates:

* Model files
* Feature metadata
* Model-performance metrics
* Processed feature data

The generated model files are stored in:

```text
models/
```

---

## Run the Demo Prediction

After training the models, run:

```bash
python scripts/run_demo.py
```

This returns a sample prediction containing:

* Forecasted daily demand
* Stockout probability
* Safety-stock recommendation
* Reorder point
* Recommended reorder quantity
* Inventory-cover days
* Supplier-risk score
* Anomaly score
* Expected lost sales
* Recommended business actions

---

## Run the FastAPI Backend

Start the API:

```bash
uvicorn app.api:app --reload --port 8000
```

Open the interactive API documentation:

```text
http://localhost:8000/docs
```

Open the API health endpoint:

```text
http://localhost:8000/health
```

---

## API Endpoints

### Health Check

```http
GET /health
```

### Model Metrics

```http
GET /model-metrics
```

### Supply-Chain Prediction

```http
POST /predict
```

Example request:

```json
{
  "features": {
    "units_sold": 35,
    "opening_inventory": 75,
    "closing_inventory": 40,
    "unit_cost": 85,
    "selling_price": 145,
    "supplier_lead_time_days": 12,
    "supplier_reliability": 0.88,
    "promotion_flag": 1,
    "holiday_flag": 0,
    "weather_index": 0.2,
    "supplier_delay_flag": 1,
    "returned_units": 1,
    "demand_lag_1": 38,
    "demand_lag_7": 32,
    "demand_lag_14": 30,
    "demand_lag_30": 28,
    "demand_roll_mean_7": 34,
    "demand_roll_std_7": 5,
    "demand_roll_mean_14": 31,
    "demand_roll_std_14": 6,
    "demand_roll_mean_30": 29,
    "demand_roll_std_30": 7,
    "inventory_cover_days": 1.18,
    "supplier_risk": 0.42,
    "year": 2026,
    "month": 7,
    "quarter": 3,
    "day_of_week": 2,
    "day_of_year": 200
  }
}
```

### Scenario Simulation

```http
POST /scenario
```

Example request:

```json
{
  "baseline_demand": 100,
  "current_inventory": 80,
  "demand_change_pct": 20,
  "lead_time_change_pct": 15,
  "promotion_uplift_pct": 10,
  "transfer_quantity": 25
}
```

---

## Run the Streamlit Dashboard

Open another terminal and run:

```bash
streamlit run app/dashboard.py
```

Open the dashboard:

```text
http://localhost:8501
```

The dashboard includes:

* Product selection
* Store selection
* Forecasted demand
* Stockout probability
* Recommended reorder quantity
* Safety stock
* Reorder point
* Inventory-cover days
* Expected lost sales
* Demand and inventory trends
* Supplier-risk indicators
* Anomaly indicators
* Regional stockout exposure
* Scenario simulation
* Automated recommendations

---

## Model Evaluation

The project evaluates the demand model using:

* Mean Absolute Error
* Root Mean Squared Error
* R-squared

The stockout model is evaluated using:

* Accuracy
* ROC-AUC

The evaluation process uses time-based train and test separation to reduce data leakage.

---

## Run Automated Tests

Run:

```bash
pytest
```

The tests cover:

* Dataset loading
* Inventory calculations
* Reorder quantity logic
* Stockout-risk classification
* Scenario simulation
* Inventory-transfer effects

---

## Docker Deployment

Build and run the services:

```bash
docker compose up --build
```

The services will be available at:

```text
FastAPI: http://localhost:8000
Streamlit: http://localhost:8501
```

---

## Business Value

SupplyChainIQ AI can help organizations:

* Reduce stockouts
* Reduce lost sales
* Improve supplier planning
* Lower inventory holding costs
* Improve replenishment decisions
* Increase inventory visibility
* Detect unusual demand patterns
* Improve service levels
* Support data-driven purchasing decisions
* Improve coordination across stores and regions

---

## Future Improvements

The project can be extended with:

* Temporal Fusion Transformer
* LSTM demand forecasting
* LightGBM model comparison
* SHAP model explanations
* Linear programming for inventory allocation
* Multi-warehouse optimization
* Real-time Kafka or MQTT ingestion
* PostgreSQL or time-series database integration
* ERP integration
* Supplier API integration
* Automated email or Slack alerts
* Scheduled model retraining
* Model-drift monitoring
* Cloud deployment
* Role-based access control
* Purchase-order workflow integration

---

## Limitations

* The dataset is synthetic.
* Inventory formulas are simplified.
* Supplier behavior is simulated.
* Real-world supply chains may include additional constraints.
* The models should be retrained using company-specific data.
* Business recommendations should be reviewed by supply-chain professionals before operational use.

---

## Responsible Use

This project is designed as a portfolio, research, and educational prototype.

It should support, not replace, qualified supply-chain, procurement, inventory, and operations professionals.

---

## GitHub Repository

View the complete project:

https://github.com/abbyogbebor/SupplyChainIQ.git

---

## Author

Developed as an advanced machine learning and artificial intelligence portfolio project focused on supply-chain analytics, demand forecasting, inventory optimization, and business decision support.

---

## Licence

This project is available under the MIT Licence.
