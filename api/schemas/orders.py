from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail



class OrderItemSchema(BaseModel):
    menu_item_id: int
    quantity: int

class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemSchema]

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    total_amount: float
    tax_amount: float
    status: str
    details: List[OrderDetail] = []

    class ConfigDict:
        from_attributes = True
