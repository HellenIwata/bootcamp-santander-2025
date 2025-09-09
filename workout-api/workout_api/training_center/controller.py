from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from workout_api.training_center.models import TrainingCenterModel
from workout_api.training_center.schemas import TrainingCenterPost, TrainingCenterResponse
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    "/",
    summary="Create a new training center",
    description="Endpoint to create a new training center in the system.",
    status_code=status.HTTP_201_CREATED,
    response_model=TrainingCenterResponse,
)
async def create_training_center(
    db_session: DatabaseDependency,
    training_center_post: TrainingCenterPost = Body(...)
) -> TrainingCenterResponse:
    training_center_model = TrainingCenterModel(
        id=uuid4(),
        **training_center_post.model_dump()
    )
    try:
        db_session.add(training_center_model)
        await db_session.commit()
        await db_session.refresh(training_center_model)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Training center with name {training_center_model.name} already exists."
        )

    return training_center_model


@router.get(
    "/",
    summary="List all training centers",
    description="Endpoint to list all training centers in the system.",
    status_code=status.HTTP_200_OK,
    response_model=list[TrainingCenterResponse]
)
async def get_all(
    db_session: DatabaseDependency,
) -> list[TrainingCenterResponse]:

    training_centers = (
        (await db_session.execute(
            select(TrainingCenterModel)
        )).scalars().all()
    )

    return training_centers

@router.get(
    "/{training_center_id}",
    summary="Get a training center by ID",
    description="Endpoint to retrieve a training center by its ID.",
    status_code=status.HTTP_200_OK,
    response_model=TrainingCenterResponse
)
async def get_by_id(
    training_center_id: UUID4,
    db_session: DatabaseDependency,
) -> TrainingCenterResponse:
    training_center = (
        (await db_session.execute(
            select(TrainingCenterModel).filter_by(id=training_center_id)
        )).scalars().first()
    )

    if not training_center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training center not found with id: {training_center_id}"
        )
    return training_center