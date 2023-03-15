from sqlalchemy import Column, Integer, ForeignKey, String

from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String)
