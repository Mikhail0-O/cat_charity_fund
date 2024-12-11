from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.investing import the_logic_of_investing
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
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
    the_logic_of_investing(all_uninvested_projects, new_donation)
    await donation_crud.refresh_db(session, new_donation)
    return new_donation


@router.get('/my',
            response_model=list[DonationDB],
            response_model_exclude_none=True,)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_by_user(session=session, user=user)


@router.get('/',
            response_model=list[DonationDBForSuperUsers],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)],)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    return await donation_crud.get_multi(session)
