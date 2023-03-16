from sqlalchemy import Column, String

from app.core.db import Base


class CharityProject(Base):
    name = Column(String, unique=True, nullable=False)
    comment = Column(String)
