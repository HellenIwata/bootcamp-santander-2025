from workout_api.contrib.models import BaseModel

from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import  Mapped, mapped_column, relationship


class CategoryModel(BaseModel):
    '''
    SQLAlchemy model for category data.
    '''

    __tablename__ = 'categories'

    pk_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    athletes: Mapped[list['AthleteModel']] = relationship(
        'AthleteModel',
        back_populates='category'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )