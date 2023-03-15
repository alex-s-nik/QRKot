from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings

class PreBase:
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    id = Column(Integer, primary_key=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, nullable=False)
    create_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime)
    


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session