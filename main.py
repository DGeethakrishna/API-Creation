from functions.functions import create_new_order,get_allorders,update_orders
from typing import List, Union,Dict
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel, validator
from fastapi.encoders import jsonable_encoder
import json
app = FastAPI()

class ProductDetails(BaseModel):
    product_name: str
    price: int
    quantity: int
    product_img: Dict[str, str] = {"data": "", "filename": ""}

class CreateOrderRequest(BaseModel):
    user_id: str
    product_details: List[ProductDetails]
    status: str

class Item(BaseModel):
    user_id: str
    product_details: List[ProductDetails]
    total_amount: int
    status: str
    order_date_time: datetime
    
class OrderUpdateRequest(BaseModel):
    user_id: str
    order_id: str
    status: str
    updated_order_date_time: datetime = None

    @validator('updated_order_date_time', pre=True, always=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            try:
                # Try to parse the datetime string using the custom format
                return datetime.strptime(value, '%d-%m-%Y %I:%M %p')
            except ValueError:
                # If parsing fails, return None instead
                return None
        return value


@app.post('/api/v1/order-create')
def create_order(order: CreateOrderRequest):
    # attach product images to the product details
    try:
        result = create_new_order(order)
        print(result)
        return result
    except ValueError as e:
        return {"error": str(e)}


@app.get("/api/v1/order", response_model=List[Item], summary="Retrieve all items")
def get_orders():
    # Your code to get orders
    files = get_allorders()
    return files


@app.put("/api/v1/order-update")
def update_order(update: list [OrderUpdateRequest]):
    # Your code to update an order
    # create a dictionary with the required data
    orders = [json.loads(order.json()) for order in update]
    bill = update_orders(orders)
    
   
    
    return bill

