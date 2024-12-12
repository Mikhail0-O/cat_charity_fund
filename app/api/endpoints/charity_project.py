from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_empty, check_charity_project_open_or_close,
    check_name_duplicate,
    check_name_and_full_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from core.investing import distribution_of_donations


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
    new_project = await charity_project_crud.create(charity_project, session)
    unallocated_donations = await charity_project_crud.get_uninvested(
        session, Donation
    )
    distribution_of_donations(unallocated_donations, new_project)
    await charity_project_crud.refresh_db(session, new_project)
    return new_project


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True,)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


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
    await check_name_and_full_amount(obj_in, project, session)
    await charity_project_crud.refresh_db(session, project)
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
    return await charity_project_crud.remove(
        db_obj=project,
        session=session,
    )
