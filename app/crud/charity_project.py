from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDMeetingRoom(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_project_full_amount_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_full_amount = await session.execute(
            select(CharityProject.full_amount).where(
                CharityProject.name == project_name
            )
        )
        db_project_full_amount = db_project_full_amount.scalars().first()
        return db_project_full_amount


charity_project_crud = CRUDMeetingRoom(CharityProject)
