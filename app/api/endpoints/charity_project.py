from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB,
    CharityProjectUpdate)
from app.core.db import get_async_session
from app.api.validators import (
    check_name_duplicate, check_charity_project_open_or_close,
    check_charity_project_empty,
    check_project_full_amount_not_lt_full_amount_current)
from app.core.user import current_superuser

router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)],)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    await check_name_duplicate(charity_project.name, session)
    new_room = await charity_project_crud.create(charity_project, session)
    return new_room


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True,)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session),
):
    all_rooms = await charity_project_crud.get_multi(session)
    return all_rooms


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)],
              response_model_exclude_none=True,)
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    project = await check_charity_project_open_or_close(
        project_id, session
    )
    print(obj_in.dict())
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    project = await charity_project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session,
    )
    if obj_in.full_amount is not None:
        await check_project_full_amount_not_lt_full_amount_current(
            project_id, obj_in.dict(), session
        )
        if obj_in.full_amount == project.invested_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
    await session.commit()
    await session.refresh(project)
    return project


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)],)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    project = await check_charity_project_open_or_close(
        project_id, session
    )
    project = await check_charity_project_empty(
        project_id, session
    )
    project = await charity_project_crud.remove(
        db_obj=project,
        session=session,
    )
    return project
