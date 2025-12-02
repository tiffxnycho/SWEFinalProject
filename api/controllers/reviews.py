from sqlalchemy.orm import Session
from api.models.reviews import ReviewDB

def get_all_reviews(db: Session):
    # manager sees all reviews, lowest-rated first
    return (
        db.query(ReviewDB)
        .order_by(ReviewDB.rating.asc())
        .all()
    )