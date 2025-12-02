from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(DECIMAL(6, 2), nullable=False)
    method = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, server_default="PENDING")
    created_at = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    order = relationship("Order", back_populates="payments")