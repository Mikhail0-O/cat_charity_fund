from datetime import datetime

from sqlalchemy import Column, Text, Integer, Boolean, DateTime, ForeignKey

from app.core.db import Base
from app.models.base import BaseModel


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
