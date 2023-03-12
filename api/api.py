from functions.functions import create_new_order
from fastapi import FastAPI, APIRouter

app = FastAPI()
api_app = APIRouter()

# Your routes here

app.include_router(api_app)



@app.post('/api/v1/order-create')
def create_order(order: dict):
    # attach product images to the product details
    try:
        result = create_new_order(order)
        return result
    except ValueError as e:
        return {"error": str(e)}


@app.get("/api/v1/order")
def get_orders():
    # Your code to get orders
    return {"message": "Orders retrieved successfully"}


@app.put("/api/v1/order-update")
def update_order(order_id: str, update_fields: dict):
    # Your code to update an order
    return {"message": "Order updated successfully"}