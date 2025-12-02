
from pydantic import BaseModel

class ReviewOut(BaseModel):
    id: int
    menu_item_id: int
    rating: int
    comment: str | None = None

    class Config:
        orm_mode = True
