from typing import Optional
from datetime import timedelta

from sqlalchemy import select, asc, func
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
        return db_project_id.scalars().first()

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
        return db_project_full_amount.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, int]]:
        projects = await session.execute(
            select(
                CharityProject.id,
                CharityProject.name,
                CharityProject.description,
                CharityProject.create_date,
                CharityProject.close_date,
                (
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)
                ).label('completion_time')
            ).where(
                CharityProject.fully_invested == 1,
                CharityProject.close_date.isnot(None),
            ).order_by(asc('completion_time')))
        projects = projects.all()
        result = []
        for project in projects:
            completion_timedelta = timedelta(days=project.completion_time)
            result.append({
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'completion_time': str(completion_timedelta),
            })
        return result


charity_project_crud = CRUDMeetingRoom(CharityProject)
