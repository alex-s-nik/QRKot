from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Базовый класс Пожертвования"""
    comment: Optional[str]
    full_amount: PositiveInt = 0


class DonationDBBase(DonationBase):
    """Базовый класс Пожертвования при получении объекта из БД"""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationCreate(DonationBase):
    """Создание пожертвования"""
    pass


class DonationDBForSuperUser(DonationDBBase):
    """Представление Пожертвования при запросе из БД для суперпользователя"""
    user_id: int
    invested_amount: PositiveInt = 0
    fully_invested: bool = False
    close_date: Optional[datetime]


class DonationDBForUser(DonationDBBase):
    """Представление Пожертвования при запросе из БД
    для обычного пользователя
    """
    pass
