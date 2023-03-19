from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """Базовый класс Проекта"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        orm_mode = True
        extra = Extra.forbid
        min_anystr_length = 1

class CharityProjectCreate(CharityProjectBase):
    """Создание Проекта"""
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt



class CharityProjectUpdate(CharityProjectBase):
    """Обновление Проекта"""
    @validator('name')
    def name_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Название проекта не может быть пустым!')
        return value

class CharityProjectFromDB(CharityProjectBase):
    """Представление Проекта при запросе из БД"""
    id: int
    invested_amount: NonNegativeInt
    create_date: datetime
    fully_invested: bool
    close_date: Optional[datetime]
