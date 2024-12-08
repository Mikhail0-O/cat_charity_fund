from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):
    pass

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ):
        donations = await session.execute(
            # Получить все объекты Reservation.
            select(Donation).where(
                Donation.user_id == user.id,
            )
        )
        print(user.id, type(Donation.user_id))
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
