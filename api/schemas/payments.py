from datetime import datetime
from pydantic import BaseModel, Field


class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0, description="Payment amount must be greater than zero")
    method: str = Field(..., min_length=1, description="Payment method, e.g. 'CASH', 'CARD'")


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int
    order_id: int
    status: str
    payment_date: datetime

    class ConfigDict:
        from_attributes = True