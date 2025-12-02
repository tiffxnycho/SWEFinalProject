from pydantic import BaseModel

class MenuItem(BaseModel):
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True