from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float

class MenuItemCreate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True