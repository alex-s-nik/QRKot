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
    """Получить список всех проектов. Доступно всем посетителям сайта."""
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
    """Создать новый проект. Может только суперпользователь."""
    project_id_from_db = await charity_project_crud.get_project_id_by_name(project.name)
    if project_id_from_db:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='ПРоект с таким именем уже существует!'
        )
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
    """Обновить данные проекта с id project_id. Доступно супрепользователю."""
    project = await charity_project_crud.get_project_by_id(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проекта с таким именем нет!'
        )
    
    project = await charity_project_crud.update(
        project, project_from_req, session
    )

    return project

@router.delete(
    '/{project_id}',
    response_model=CharityProjectFromDB
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectFromDB:
    """Удалить проект. Доступно только суперпользователю."""
    project = charity_project_crud.get_project_by_id(
        project_id, session
    )
    project = await charity_project_crud.delete(
        project, session
    )
    return project
