from sqlalchemy import Column, Integer, String, Float
# You need to import 'Base' from wherever your database connection is defined.
# Open your 'api/models/orders.py' and copy the import line that imports 'Base'.
# It usually looks like: from ..database import Base
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(255))
    price = Column(Float)