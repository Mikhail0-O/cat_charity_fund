from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime

from app.core.db import Base
from app.models.base import BaseModel


class CharityProject(BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
