from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.model_service import SupplyChainService


app = FastAPI(
    title="SupplyChainIQ AI API",
    description="Demand forecasting, stockout risk, inventory optimization, and scenario simulation.",
    version="1.0.0",
)

service = None


class PredictionRequest(BaseModel):
    features: dict[str, float]


class ScenarioRequest(BaseModel):
    baseline_demand: float
    current_inventory: float
    demand_change_pct: float = 0
    lead_time_change_pct: float = 0
    promotion_uplift_pct: float = 0
    transfer_quantity: float = 0


@app.on_event("startup")
def startup():
    global service
    if (Path(__file__).resolve().parents[1] / "models" / "metadata.json").exists():
        service = SupplyChainService()


@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": service is not None}


@app.get("/model-metrics")
def model_metrics():
    if service is None:
        raise HTTPException(503, "Models are not trained.")
    return service.metrics


@app.post("/predict")
def predict(request: PredictionRequest):
    if service is None:
        raise HTTPException(503, "Run python scripts/train_models.py first.")
    return service.predict(request.features)


@app.post("/scenario")
def scenario(request: ScenarioRequest):
    if service is None:
        raise HTTPException(503, "Run python scripts/train_models.py first.")
    return service.scenario(**request.model_dump())
