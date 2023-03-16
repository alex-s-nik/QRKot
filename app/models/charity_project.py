from sqlalchemy import Column, String

from app.models.base import BaseModel as Base


class CharityProject(Base):
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
