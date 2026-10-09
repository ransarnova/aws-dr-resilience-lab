from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI(title="AWS DR Resilience Lab")

orders = {}


class OrderRequest(BaseModel):
    product: str
    quantity: int


@app.get("/health/live")
def liveness():
    return {"status": "alive"}


@app.get("/health/ready")
def readiness():
    return {"status": "ready"}


@app.post("/orders", status_code=201)
def create_order(order: OrderRequest):
    order_id = str(uuid4())

    orders[order_id] = order.model_dump()

    return {
        "order_id": order_id,
        "status": "created",
    }


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")

    return orders[order_id]
