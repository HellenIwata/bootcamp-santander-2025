from workout_api.contrib.models import BaseModel

from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import  Mapped, mapped_column, relationship


class TrainingCenterModel(BaseModel):
    '''
    SQLAlchemy model for category data.
    '''

    __tablename__ = 'training_centers'

    pk_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    property_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    athletes: Mapped[list['AthleteModel']] = relationship(
        'AthleteModel',
        back_populates='training_center'
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