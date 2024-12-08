from typing import Optional
from datetime import datetime

from pydantic import (BaseModel, Field,
                      validator, Extra,
                      PositiveInt, StrictStr, root_validator)


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt

    @validator('description')
    def description_cannot_be_null(cls, value):
        if not value:
            raise ValueError(
                'Описание проекта не может быть пустым!'
            )
        return value


class CharityProjectDB(CharityProjectCreate):
    name: str = Field(None, min_length=1, max_length=100)
    description: str
    full_amount: int
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[StrictStr]
    full_amount: Optional[int] = Field(None,)

    @root_validator(skip_on_failure=True)
    def check_empty_fields(cls, values):
        if values.get('name') == '':
            raise ValueError('Поле "name" не может быть пустым.')
        if values.get('description') == '':
            raise ValueError('Поле "description" не может быть пустым.')
        return values

    class Config:
        extra = Extra.forbid
