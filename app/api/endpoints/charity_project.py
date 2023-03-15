from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectFromDB,
    CharityProjectUpdate
)

router = APIRouter(
    prefix='/charity_project',
    tags=['Charity Projects'],
)

@router.get(
    '/',
    response_model=list[CharityProjectFromDB],
    dependencies=[Depends(current_user)]
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
) -> list[CharityProjectFromDB]:
    all_projects = await charity_project_crud.get_all(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectCreate,
    dependencies=[Depends(current_superuser)]
)
async def create_new_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectFromDB:
    # await check_for_duplicates
    new_project = await charity_project_crud.create(project, session)
    return new_project

@router.patch(
    '/{project_id}',
    response_model=CharityProjectFromDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
    project_id: int,
    project_from_req: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectFromDB:
    #project = await get_project_by_id()
    '''if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проекта с таким именем нет!'
        )
    if project_from_req.<unique_field>:
        check_duplicate

    project = await charity_project_crud.update(
        project, project_from_req, session
    )

    return project'''

@router.delete(
    '/{project_id}',
    response_model=CharityProjectFromDB
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectFromDB:
    project = ...
    '''meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await delete_meeting_room(
        meeting_room, session
    )
    return meeting_room'''
    return project
