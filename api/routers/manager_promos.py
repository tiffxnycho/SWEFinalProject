from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas.promos import PromoCreate, PromoOut
from api.controllers.promos import create_promo

router = APIRouter(
    prefix="/manager/promo",
    tags=["Manager Promo Codes"],
)


@router.post("/", response_model=PromoOut)
def create_promo_endpoint(
    promo: PromoCreate,
    db: Session = Depends(get_db),
):
    return create_promo(db, promo)
