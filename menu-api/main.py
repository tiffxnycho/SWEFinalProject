from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

engine = create_engine('sqlite:///menu.db')
SessionLocal  = sessionmaker(bind=engine)
Base = declarative_base()

class MenuItemDB(Base):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

class MenuItem(BaseModel):
    name: str
    description: str
    price: float

Base.metadata.create_all(bind=engine)

@app.get("/menu-items")
def create_items(item: MenuItem):
    db = SessionLocal()
    db_item = MenuItemDB(name=item.name, description=item.description, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

@app.get("/menu-items", response_model=List[MenuItem])
def get_items():
    db = SessionLocal()
    db_items = db.query(MenuItemDB).all()
    db.close()
    return items

@app.get("/menu-items/{item_id}")
def update_item(item_id: int, item: MenuItem):
    db = SessionLocal()
    db_item = db.query(MenuItemDB).filter(MenuItemDB.id == item_id).first()
    if not db_item:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item


@app.get("/menu-items/{item_id}")
def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(MenuItemDB).filter(MenuItemDB.id == item_id).first()
    if not db_item:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item deleted"}




