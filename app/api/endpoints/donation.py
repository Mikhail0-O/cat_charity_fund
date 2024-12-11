from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import (DonationCreate, DonationDB,
                                  DonationDBForSuperUsers)


router = APIRouter()


@router.post('/',
             response_model=DonationDB,
             response_model_exclude_none=True,)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Только для зарегистрированных пользователей."""

    new_donation = await donation_crud.create(
        donation, session, user
    )
    all_uninvested_projects = await donation_crud.get_uninvested_projects(
        session
    )
    for project in all_uninvested_projects:
        donation_change = (
            new_donation.full_amount - new_donation.invested_amount
        )
        project_change = project.full_amount - project.invested_amount

        if donation_change >= project_change:
            new_donation.invested_amount += project_change
            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.now()
        else:
            project.invested_amount += donation_change
            new_donation.invested_amount = new_donation.full_amount
            new_donation.fully_invested = True
            new_donation.close_date = datetime.now()
            break
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get('/my',
            response_model=list[DonationDB],
            response_model_exclude_none=True,)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    all_donation = await donation_crud.get_by_user(session=session, user=user)
    return all_donation


@router.get('/',
            response_model=list[DonationDBForSuperUsers],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)],)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations
