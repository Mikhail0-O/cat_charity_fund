from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_empty, check_charity_project_open_or_close,
    check_name_duplicate, check_project_full_amount_not_lt_full_amount_current)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)


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
    unallocated_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False # noqa
        ).order_by(Donation.create_date)
    )
    sum_unallocated_donations = sum(
        [unallocated_donation.full_amount for unallocated_donation
            in unallocated_donations.scalars().all()]
    )
    if sum_unallocated_donations >= new_project.full_amount:
        new_project.fully_invested = True
        new_project.close_date = datetime.now()
    await session.commit()
    await session.refresh(new_project)
    return new_project


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
