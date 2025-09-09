''' 
Models and Schemas for Athlete data representation.
'''

from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from workout_api.contrib.models import BaseModel

class AthleteModel(BaseModel):
    '''
    SQLAlchemy model for athlete data.
    '''

    __tablename__ = 'athletes'

    pk_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    document: Mapped[str] = mapped_column(
        String(14),
        unique=True,
        nullable=False
    )
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    height: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    gender: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )  

    category: Mapped['CategoryModel'] = relationship(
        'CategoryModel',
        back_populates='athletes',
        lazy='selectin'
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.pk_id'),
        nullable=False
    )

    training_center: Mapped['TrainingCenterModel'] = relationship(
        'TrainingCenterModel',
        back_populates='athletes',
        lazy='selectin'
    )

    training_center_id: Mapped[int] = mapped_column(
        ForeignKey('training_centers.pk_id'),
        nullable=False
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
