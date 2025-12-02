from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas.menu_items import MenuItem
from api.controllers.menu_items import (
    create_menu_item,
    update_menu_item,
    delete_menu_item,
)

router = APIRouter(prefix="/manager/menu-items", tags=["Manager Menu Items"])

@router.post("/", response_model=MenuItem)
def create_manager_menu_item(item: MenuItem, db: Session = Depends(get_db)):
    #manager creates a new menu item
    return create_menu_item(db, item)

@router.put("/{item_id}", response_model=MenuItem)
def update_manager_menu_item(item_id: int, item: MenuItem, db: Session = Depends(get_db)):
    #manager updates current menu item
    return update_menu_item(db, item_id, item)

@router.delete("/{item_id}")
def delete_manager_menu_item(item_id: int, db: Session = Depends(get_db)):
    #manager deletes menu item
    return delete_menu_item(db, item_id)