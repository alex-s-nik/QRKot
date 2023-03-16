from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, Integer

class BaseModel:
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime)
