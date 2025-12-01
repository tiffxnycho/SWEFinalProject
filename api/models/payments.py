from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime

from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(DECIMAL(6, 2), nullable=False)
    method = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="COMPLETED")
    payment_date = Column(DATETIME, nullable=False, default=datetime.now)

    order = relationship("Order", back_populates="payments")