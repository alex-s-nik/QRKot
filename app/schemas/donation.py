from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    """Базовый класс Пожертвования"""
    comment: Optional[str]
    full_amount: PositiveInt
    
    class Config:
        extra = Extra.forbid
        orm_mode = True


class DonationDBBase(DonationBase):
    """Базовый класс Пожертвования при получении объекта из БД"""
    id: int
    create_date: datetime



class DonationCreate(DonationBase):
    """Создание пожертвования"""
    pass


class DonationDBForSuperUser(DonationDBBase):
    """Представление Пожертвования при запросе из БД для суперпользователя"""
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    # Странная ситуация: в ТЗ указано, что суперпользователь может просматривать
    # список всех пожертвований, при этом ему выводятся все поля модели,
    # а в тестах проверяются все поля, кроме close_date
    # tests/test_donation.py:102
    #  
    # close_date: Optional[datetime] 


class DonationDBForUser(DonationDBBase):
    """Представление Пожертвования при запросе из БД
    для обычного пользователя
    """
    pass
