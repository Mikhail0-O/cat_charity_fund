from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from http import HTTPStatus


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    """Проверка на уникальность названия проекта."""

    project_id = await charity_project_crud.get_project_id_by_name(
        room_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_open_or_close(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Существование проекта, проект не проинвестирован или не закрыт.

    Валидация следующих случаев:
    1) Проект с переданным id существует в базе данных.
    2) Проект не проинвестирован.
    3) Проект не закрыт.
    """

    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!'
        )
    if charity_project.invested_amount == charity_project.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Невозможно редактировать или '
                    'удалять проинвестированный проект!')
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Невозможно редактировать или '
                    'удалять закрытый проект!')
        )
    return charity_project


async def check_charity_project_empty(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Невозможно редактировать или '
                    'удалять проект с пожертвованиями!')
        )
    return charity_project


async def check_project_full_amount_not_lt_full_amount_current(
        project_id: int, obj, session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if (obj['full_amount'] < charity_project.invested_amount):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=('Невозможно редактировать требуемую сумму '
                    'если новая меньше текущей')
        )
