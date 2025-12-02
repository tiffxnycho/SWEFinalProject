from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.dependencies.database import Base
from api.models.sandwiches import SandwichDB

class ReviewsDB(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, mullable=False)

    menu_item = relationship("SandwichDB", back_populates="reviews")