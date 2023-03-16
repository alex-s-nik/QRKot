from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    """Базовый класс Проекта"""
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt = 0

    class Config:
        orm_mode = True
        extra = Extra.forbid
        min_anystr_length = 1

class CharityProjectCreate(CharityProjectBase):
    """Создание Проекта"""
    pass


class CharityProjectUpdate(CharityProjectBase):
    """Обновление Проекта"""
    pass


class CharityProjectFromDB(CharityProjectBase):
    """Представление Проекта при запросе из БД"""
    id: int
    invested_amount: PositiveInt
    create_date: datetime
    fully_invested: bool
    close_date: Optional[datetime]
