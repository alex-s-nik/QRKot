from sqlalchemy import Column, String

from app.core.db import Base


class CharityProject(Base):
    name = Column(String)
    comment = Column(String)
