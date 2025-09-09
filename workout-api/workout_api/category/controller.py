from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from workout_api.category.models import CategoryModel
from workout_api.category.schemas import CategoryPost, CategoryResponse
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    "/",
    summary="Create a new category",
    description="Endpoint to create a new category in the system.",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse,
)
async def create_category(
    db_session: DatabaseDependency,
    category_post: CategoryPost = Body(...)
) -> CategoryResponse:
    category_model = CategoryModel(id=uuid4(), **category_post.model_dump())
    try:
        db_session.add(category_model)
        await db_session.commit()
        await db_session.refresh(category_model)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Category with name {category_model.name} already exists."
        )
    return category_model


@router.get(
    "/",
    summary="List all categories",
    description="Endpoint to list all categories in the system.",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryResponse]
)
async def get_all(
    db_session: DatabaseDependency,
) -> list[CategoryResponse]:
    categories = (
        (await db_session.execute(select(CategoryModel))).scalars().all()
    )
    return categories


@router.get(
    "/{category_id}",
    summary="Get category by ID",
    description="Endpoint to retrieve a category by its ID.",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse
)
async def get_by_id(
    category_id: UUID4,
    db_session: DatabaseDependency,
) -> CategoryResponse:
    category = (
        (await db_session.execute(
            select(CategoryModel).filter_by(id=category_id)
        )).scalars().first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category not found with id: {category_id}"
        )
    return category
