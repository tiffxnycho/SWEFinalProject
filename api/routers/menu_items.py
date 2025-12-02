from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas.menu_items import MenuItem
from api.controllers.menu_items import (
    create_menu_item,
    get_all_menu_items,
    get_menu_item_by_id,
    update_menu_item,
    delete_menu_item,
)

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])


@router.post("/", response_model=MenuItem)
def create(item: MenuItem, db: Session = Depends(get_db)):
    return create_menu_item(db, item)


@router.get("/", response_model=list[MenuItem])
def list_items(db: Session = Depends(get_db)):
    return get_all_menu_items(db)


@router.get("/{item_id}", response_model=MenuItem)
def get_one(item_id: int, db: Session = Depends(get_db)):
    return get_menu_item_by_id(db, item_id)


@router.put("/{item_id}", response_model=MenuItem)
def update(item_id: int, item: MenuItem, db: Session = Depends(get_db)):
    return update_menu_item(db, item_id, item)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return delete_menu_item(db, item_id)