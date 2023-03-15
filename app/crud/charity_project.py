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
    ) -> CharityProject:
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
        project_from_db: CharityProjectFromDB,
        project_from_req: CharityProjectUpdate,
        session: AsyncSession
    ) -> CharityProject:
        project_data = jsonable_encoder(project_from_db)
        project_data_for_update = project_from_req.dict()

        for field in project_data:
            if field in project_data_for_update:
                setattr(project_from_db, field, project_data_for_update[field])

        session.add(project_from_db)
        await session.commit()
        await session.refresh(project_from_db)
        return project_from_db
    
    async def delete(
        project_from_db: CharityProjectFromDB,
        session: AsyncSession,            
    ) -> CharityProject:
        await session.delete(project_from_db)
        await session.commit()
        return project_from_db

charity_project_crud = CRUDCharityProject()
