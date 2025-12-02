from sqlalchemy import Column, Integer, String, Float
from api.dependencies.database import Base   # reuse your existing Base

class MenuItemDB(Base):
    __tablename__ = "menu_items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)