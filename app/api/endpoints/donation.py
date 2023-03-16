from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDBForSuperUser,
    DonationDBForUser
)


router = APIRouter(
    prefix='/donation',
    tags=['Donations'],
)


@router.post(
    '/',
    response_model=DonationCreate,
    dependencies=[Depends(current_user)]
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session)
) -> DonationDBForUser:
    """Сделать пожертвование. Доступно любому пользователю."""
    new_donation = await donation_crud.create(donation, session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDBForSuperUser],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
) -> Optional[list[DonationDBForSuperUser]]:
    """Получить все пожертвования. Доступно только суперпользователю."""
    all_donations = await donation_crud.get_all(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDBForUser],
    dependencies=[Depends(current_user)]
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> Optional[list[DonationDBForUser]]:
    """Получить все пожартвования текущего пользователя."""
    my_donations = await donation_crud.get_my(session, user)
    return my_donations
