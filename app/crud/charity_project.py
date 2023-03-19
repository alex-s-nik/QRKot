from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectFromDB,
    CharityProjectUpdate
)


class CRUDCharityProject:
    async def create(
        self,
        new_project: CharityProjectCreate,
        session: AsyncSession
    ) -> CharityProjectFromDB:
        new_project_data = new_project.dict()

        db_project = CharityProject(**new_project_data)

        session.add(db_project)

        await session.commit()
        await session.refresh(db_project)
        return db_project

    async def get_all(
        self,
        session: AsyncSession
    ) -> Optional[list[CharityProject]]:
        db_projects = await session.execute(
            select(CharityProject)
        )
        return db_projects.scalars().all()

    async def update(
        self,
        project_from_db: CharityProjectFromDB,
        project_from_req: CharityProjectUpdate,
        session: AsyncSession
    ) -> CharityProject:
        project_data = jsonable_encoder(project_from_db)
        project_data_for_update = project_from_req.dict(exclude_unset=True)

        for field in project_data:
            if field in project_data_for_update:
                setattr(project_from_db, field, project_data_for_update[field])

        session.add(project_from_db)
        await session.commit()
        await session.refresh(project_from_db)
        return project_from_db

    async def delete(
        self,
        project_from_db: CharityProjectFromDB,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(project_from_db)
        await session.commit()
        return project_from_db

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_project_by_id(
        self,
        project_id: int,
        session: AsyncSession
    ) -> Optional[CharityProject]:
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )
        return project.scalars().first()


charity_project_crud = CRUDCharityProject()
