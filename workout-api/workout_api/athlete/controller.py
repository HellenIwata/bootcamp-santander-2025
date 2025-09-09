from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from workout_api.athlete.models import AthleteModel
from workout_api.athlete.schemas import AthletePost, AthleteResponse, AthleteShort, AthleteUpdate
from workout_api.category.models import CategoryModel
from workout_api.training_center.models import TrainingCenterModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Create a new athlete",
    description="Endpoint to create a new athlete in the system.",
    status_code=status.HTTP_201_CREATED,
    response_model=AthleteResponse,
)
async def create_athlete(
    db_session: DatabaseDependency,
    athlete_post: AthletePost = Body(...)
) -> AthleteResponse:
    category_name = athlete_post.category_name
    training_center_name = athlete_post.training_center_name

    category = (
        await db_session.execute(
            select(CategoryModel).filter_by(name=category_name)
    )).scalars().first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category not found: {category_name}")

    training_center = (
        await db_session.execute(
            select(TrainingCenterModel).filter_by(name=training_center_name)
    )).scalars().first()

    if not training_center:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Training Center not found: {training_center_name}")

    try:
        athlete_data = athlete_post.model_dump(exclude={'category_name', 'training_center_name'})
        athlete_model = AthleteModel(
            id=uuid4(),
            **athlete_data,
            category_id=category.pk_id,
            training_center_id=training_center.pk_id
        )
        db_session.add(athlete_model)
        await db_session.commit()
        await db_session.refresh(athlete_model)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {athlete_post.document}"
        )

    return athlete_model

@router.patch(
    "/{athlete_id}",
    summary="Update an athlete by ID",
    description="Endpoint to update an existing athlete by their unique ID.",
    status_code=status.HTTP_200_OK,
    response_model=AthleteResponse,
)
async def update_athlete(
    athlete_id: UUID4,
    db_session: DatabaseDependency,
    athlete_update: AthleteUpdate = Body(...)
) -> AthleteResponse:
    athlete = (
        (await db_session.execute(
            select(AthleteModel).filter_by(id=athlete_id)
        )).scalars().first()
    )

    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID Athlete not found: {athlete_id}"
        )
    
    athlete_data = athlete_update.model_dump(exclude_unset=True)

    if category_name := athlete_data.get('category_name'):
        category = (await db_session.execute(select(CategoryModel).filter_by(name=category_name))).scalars().first()
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category not found: {category_name}")
        athlete.category_id = category.pk_id

    if training_center_name := athlete_data.get('training_center_name'):
        training_center = (await db_session.execute(select(TrainingCenterModel).filter_by(name=training_center_name))).scalars().first()
        if not training_center:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Training Center not found: {training_center_name}")
        athlete.training_center_id = training_center.pk_id

    for key, value in athlete_data.items():
        if key not in ['category_name', 'training_center_name']:
            setattr(athlete, key, value)

    # Note: The IntegrityError for 'document' is not handled here because 'document' is not part of AthleteUpdate.
    # This is good practice, as unique identifiers like CPF should generally not be updatable via PATCH.

    await db_session.commit()
    await db_session.refresh(athlete)

    return athlete


@router.get(
    "/",
    summary="Retrieve all athletes",
    description="Endpoint to retrieve a list of all athletes in the system.",
    status_code=status.HTTP_200_OK,
    response_model=Page[AthleteShort],
)
async def get_all(
    db_session: DatabaseDependency,
    name: Optional[str] = None,
    document: Optional[str] = None,
) -> Page[AthleteShort]:
    query = select(AthleteModel)

    if name:
        query = query.filter(AthleteModel.name.ilike(f'%{name}%'))

    if document:
        query = query.filter_by(document=document)

    return await paginate(db_session, query)


@router.get(
    "/{athlete_id}",
    summary="Retrieve an athlete by ID",
    description="Endpoint to retrieve a specific athlete by their unique ID.",
    status_code=status.HTTP_200_OK,
    response_model=AthleteResponse,
)
async def get_by_id(
    athlete_id: UUID4,
    db_session: DatabaseDependency,
) -> AthleteResponse:
    athlete = (
        (await db_session.execute(
            select(AthleteModel).filter_by(id=athlete_id)
        )).scalars().first()
    )
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID Athlete not found: {athlete_id}"
        )
    return athlete

@router.get(
    "/document/{athlete_document}",
    summary="Retrieve an athlete by Document",
    description="Endpoint to retrieve a specific athlete by their unique Document.",
    status_code=status.HTTP_200_OK,
    response_model=AthleteResponse,
)
async def get_by_document(
    athlete_document: str,
    db_session: DatabaseDependency,
) -> AthleteResponse:
    athlete = (
        (await db_session.execute(
            select(AthleteModel).filter_by(document=athlete_document)
        )).scalars().first()
    )
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document Athlete not found: {athlete_document}"
        )
    return athlete


add_pagination(router)
