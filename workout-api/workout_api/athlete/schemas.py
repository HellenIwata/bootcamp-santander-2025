'''
Schemas for athlete-related data.
'''

from datetime import datetime
from typing import Annotated
from pydantic import UUID4, Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.category.schemas import CategoryResponseWithAthletes
from workout_api.training_center.schemas import TrainingCenterResponseWithAthletes


class CategoryName(BaseSchema):
    name: Annotated[str, Field(description="Nome da categoria", example="Scale")]

class TrainingCenterName(BaseSchema):
    name: Annotated[str, Field(description="Nome do centro de treinamento", example="CT King")]

class AthleteShort(OutMixin):
    '''
    Schema para resposta resumida de dados do atleta.
    '''
    name: Annotated[str, Field(description="Nome do atleta", example='Joao Silva Santos')]
    category: CategoryName
    training_center: TrainingCenterName

class AthleteBase(BaseSchema):
    '''
    Base schema for athlete data.
    '''

    name: Annotated[
        str, 
        Field(
            description="The athlete's full name",
            example='Joao Silva Santos',
            max_length=50
        )
    ]

    document: Annotated[
        str, 
        Field(
            description="The athlete's document number (e.g., CPF)",
            example='12345678900',
            max_length=14,
            min_length=11
        )
    ]

    age: Annotated[
        int, 
        Field(
            description="The athlete's age",
            example=25,
            ge=0,
            le=120
        )
    ]

    weight: Annotated[
        PositiveFloat, 
        Field(
            description="The athlete's weight in kilograms",
            example=70.5
        )
    ]

    height: Annotated[
        float, 
        Field(
            description="The athlete's height in meters",
            example=1.75,
            ge=0.0,
            le=3.0
        )
    ]

    gender: Annotated[
        str, 
        Field(
            description="The athlete's gender (F-M)",
            example='M',
            max_length=1,
            min_length=1
        )
    ]


class AthletePost(AthleteBase):
    '''
    Schema for creating a new athlete.
    '''
    category_name: Annotated[
        str,
        Field(
            description="The name of the category associated with the athlete",
            example="Categoria A"
        )
    ]

    training_center_name: Annotated[
        str,
        Field(
            description="The name of the training center associated with the athlete",
            example="Centro X"
        )
    ]


class AthleteResponse(AthleteBase, OutMixin):
    '''
    Schema for athlete response data.
    '''
    category: Annotated[
        CategoryName | None,
        Field(
            description="The category associated with the athlete",
            example={"name": "Scaled"}
        )
    ]
    training_center: Annotated[
        TrainingCenterName | None,
        Field(
            description="The training center associated with the athlete",
            example={"name": "CT KING"}
        )
    ]

class AthleteUpdate(BaseSchema):
    '''
    Schema for updating an athlete.
    '''
    name: Annotated[str, Field(description="The athlete's full name", example='Joao Silva Santos', max_length=50)] | None = None
    age: Annotated[int, Field(description="The athlete's age", example=25, ge=0, le=120)] | None = None
    weight: Annotated[PositiveFloat, Field(description="The athlete's weight in kilograms", example=70.5)] | None = None
    height: Annotated[float, Field(description="The athlete's height in meters", example=1.75, ge=0.0, le=3.0)] | None = None
    category_name: Annotated[str, Field(description="The name of the category associated with the athlete", example="Categoria A")] | None = None
    training_center_name: Annotated[str, Field(description="The name of the training center associated with the athlete", example="Centro X")] | None = None