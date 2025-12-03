from pydantic import BaseModel
from datetime import date


class PromoCreate(BaseModel):
    code: str
    discount: float
    expiration: date

    class Config:
        orm_mode = True

class PromoOut(PromoCreate):
    id: int
    active: bool

