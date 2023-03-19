from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import CharityProject, Donation
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectFromDB,
    CharityProjectUpdate
)
from app.services.invest import close, invest

router = APIRouter(
    prefix='/charity_project',
    tags=['Charity Projects'],
)

@router.get(
    '/',
    response_model=list[CharityProjectFromDB],
    dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
) -> list[CharityProjectFromDB]:
    """Получить список всех проектов. Доступно всем посетителям сайта."""
    all_projects = await charity_project_crud.get_all(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectFromDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_new_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectFromDB:
    """Создать новый проект. Может только суперпользователь."""
    project_id_from_db = await charity_project_crud.get_project_id_by_name(project.name, session)
    if project_id_from_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )
    new_project = await charity_project_crud.create(project, session)
    new_project = await invest(Donation, new_project, session)
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
    project: CharityProject = await charity_project_crud.get_project_by_id(project_id, session)

    # Обновляемого проекта нет в БД
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого проекта нет!'
        )
    # Новое имя для проекта совпадает с именем существующего проекта в БД
    if project_from_req.name:
        project_db_id = await charity_project_crud.get_project_id_by_name(
            project_from_req.name, session
        )
        if project_db_id and project_db_id != project_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Проект с таким именем уже существует!'
            )
    
    # Нельзя изменить сумму необходимую для проекта на меньшую, чем уже внесено средств
    if hasattr(project_from_req, 'full_amount') and project_from_req.full_amount and project_from_req.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя сделать сумму пожертвования ниже, чем уже внесено средств.'
        )
    
    # Закрытый проект нельзя редактировать
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )

    project = await charity_project_crud.update(
        project, project_from_req, session
    )
    if hasattr(project_from_req, 'full_amount') and project_from_req.full_amount == project.invested_amount:
        project = close(project)

    return project

@router.delete(
    '/{project_id}',
    response_model=CharityProjectFromDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectFromDB:
    """Удалить проект. Доступно только суперпользователю."""
    project: CharityProject = await charity_project_crud.get_project_by_id(
        project_id, session
    )
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    project = await charity_project_crud.delete(
        project, session
    )
    return project
