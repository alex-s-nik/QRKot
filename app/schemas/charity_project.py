from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class CharityProjectBase(BaseModel):
    """Базовый класс Проекта"""
    name: str
    decription: str
    full_amount: PositiveInt = 0


class CharityProjectCreate(CharityProjectBase):
    """Создание Проекта"""
    pass


class CharityProjectUpdate(CharityProjectBase):
    """Обновление Проекта"""
    pass


class CharityProjectFromDB(CharityProjectBase):
    """Представление Проекта при запросе из БД"""
    id: int
    invested_amount: PositiveInt = 0
    create_date: datetime
    fully_invested: bool = False
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
