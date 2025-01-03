from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id,
            )
        )
        return donations.scalars().all()

    # async def get_uninvested_projects(
    #         self,
    #         session: AsyncSession,
    # ):
    #     uninvested_projects = await session.execute(
    #         select(CharityProject).where(
    #             CharityProject.fully_invested == False # noqa 

    #         ).order_by(CharityProject.create_date)
    #     )
    #     return uninvested_projects.scalars().all()


donation_crud = CRUDDonation(Donation)
