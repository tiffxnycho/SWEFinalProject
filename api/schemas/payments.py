from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class PaymentBase(BaseModel):
    amount: Decimal
    method: str


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int
    order_id: int
    status: str
    created_at: datetime

    class ConfigDict:
        from_attributes = True


class PaymentBase(BaseModel):
    amount: Decimal
    method: str
    promo_code: Optional[str] = None