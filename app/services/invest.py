from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BaseModel


def close(
        object: BaseModel
) -> BaseModel:
    object.fully_invested = True
    object.close_date = datetime.now()

    return object


async def invest(name_objects_from_db: BaseModel, obj_with_money: BaseModel, session: AsyncSession) -> BaseModel:
    all_objects_from_db = await session.execute(
        select(name_objects_from_db).where(
            name_objects_from_db.fully_invested is False
        ).order_by(name_objects_from_db.create_date)
    )
    all_objects_from_db = all_objects_from_db.scalars().all()

    for obj in all_objects_from_db:
        obj_needed_amount = obj.full_amount - obj.invested_amount
        available_money = obj_with_money.full_amount - obj_with_money.invested_amount

        if available_money <= obj_needed_amount:
            obj.invested_amount += available_money
            if obj.invested_amount == obj.full_amount:
                obj = close(obj)
            obj_with_money.invested_amount = obj_with_money.full_amount
            obj_with_money = close(obj_with_money)
            session.add(obj)
            break

        obj_with_money.invested_amount += obj_needed_amount
        obj.invested_amount = obj.full_amount
        obj = close(obj)
        session.add(obj)
        session.add(obj_with_money)

    await session.commit()
    await session.refresh(obj_with_money)
    return obj_with_money
