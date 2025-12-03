from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from api.models.reviews import ReviewsDB


def get_all_reviews(db: Session):
    """
    Return all reviews for the manager, lowest-rated first.
    """
    try:
        return (
            db.query(ReviewsDB)
            .order_by(ReviewsDB.rating.asc())
            .all()
        )
    except SQLAlchemyError as e:
        # Convert DB errors to a 400 instead of a 500
        error = str(getattr(e, "orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )