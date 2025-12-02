from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.models.menu_items import MenuItemDB
from api.schemas.menu_items import MenuItem

def create_menu_item(db: Session, item: MenuItem):
    db_item = MenuItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_all_menu_items(db: Session):
    return db.query(MenuItemDB).all()


def get_menu_item_by_id(db: Session, item_id: int):
    item = db.query(MenuItemDB).filter(MenuItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def update_menu_item(db: Session, item_id: int, item: MenuItem):
    db_item = db.query(MenuItemDB).filter(MenuItemDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_menu_item(db: Session, item_id: int):
    db_item = db.query(MenuItemDB).filter(MenuItemDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}