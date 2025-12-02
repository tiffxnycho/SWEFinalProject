from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..dependencies.database import get_db
from ..models import menu as model
from ..schemas import menu as schema


router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)



@router.post("/", response_model=schema.MenuItem)
def create_menu_item(item: schema.MenuItemCreate, db: Session = Depends(get_db)):
    new_item = model.MenuItem(
        name=item.name,
        description=item.description,
        price=item.price
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item



@router.get("/", response_model=List[schema.MenuItem])
def read_menu_items(db: Session = Depends(get_db)):
    return db.query(model.MenuItem).all()



@router.get("/{item_id}", response_model=schema.MenuItem)
def read_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item



@router.put("/{item_id}", response_model=schema.MenuItem)
def update_menu_item(item_id: int, item_update: schema.MenuItemCreate, db: Session = Depends(get_db)):
    item_db = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
    if item_db is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    item_db.name = item_update.name
    item_db.description = item_update.description
    item_db.price = item_update.price

    db.commit()
    db.refresh(item_db)
    return item_db



@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    item_db = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
    if item_db is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db.delete(item_db)
    db.commit()
    return None