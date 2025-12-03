from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, Boolean
from datetime import datetime

from ..dependencies.database import Base

class Promo(Base):
    __tablename__ = "promos"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    # 0.20 = 20% off
    discount = Column(DECIMAL(4, 2), nullable=False)
    expiration = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    active = Column(Boolean, nullable=False, default=True)