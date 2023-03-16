from sqlalchemy import Column, Integer, ForeignKey, String

from app.models.base import BaseModel as Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(String)
