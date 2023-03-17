from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationDBForSuperUser, DonationDBForUser


class CRUDDonation:
    async def create(
            self,
            new_donation: DonationCreate,
            session: AsyncSession,
            user: User
    ) -> DonationDBForUser:
        new_donation_data = new_donation.dict()
        new_donation_data['user_id'] = user.id

        db_donation = Donation(**new_donation_data)

        session.add(db_donation)

        await session.commit()
        await session.refresh(db_donation)
        return db_donation
    
    async def get_all(
        self,
        session: AsyncSession
    ) -> Optional[list[DonationDBForSuperUser]]:
        db_donations = await session.execute(select(Donation))
        return db_donations.scalars().all()
    
    async def get_my(
        self,
        session: AsyncSession,
        user: User
    ) -> Optional[list[DonationDBForUser]]:
        db_my_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return db_my_donations.scalars().all()

donation_crud = CRUDDonation()
