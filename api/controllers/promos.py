from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.models.promos import Promo
from api.schemas.promos import PromoCreate


def create_promo(db: Session, promo_in: PromoCreate) -> Promo:
    # Ensure code is stored uppercase and unique
    code = promo_in.code.upper()
    existing = db.query(Promo).filter(Promo.code == code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Promo code already exists")

    promo = Promo(
        code=code,
        discount=promo_in.discount,
        expiration=promo_in.expiration,
        active=True
    )
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo


def get_valid_promo(db: Session, code: str) -> Promo | None:
    """Return a promo if it exists, is active, and not expired."""
    today = date.today()
    return (
        db.query(Promo)
        .filter(
            Promo.code == code.upper(),
            Promo.active.is_(True),
            Promo.expiration >= today,
        )
        .first()
    )
