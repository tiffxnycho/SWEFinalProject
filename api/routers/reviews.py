from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas.reviews import ReviewOut
from api.controllers.reviews import get_all_reviews

router = APIRouter(prefix="/manager/reviews", tags=["Reviews"])

@router.get("/", response_model=list[ReviewOut])
def list_reviews(db: Session = Depends(get_db)):
    return get_all_reviews(db)