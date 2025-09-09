'''
Schemas for Training-Center-related data.
'''

from datetime import datetime
from typing import Annotated
from pydantic import UUID4, Field

from workout_api.category.schemas import CategoryPost
from workout_api.contrib.schemas import BaseSchema, OutMixin

class TrainingCenterBase(BaseSchema):
    '''
    Base schema for Training Center data.
    '''

    name: Annotated[
        str, 
        Field(
            description="The training center's full name",
            example='CT KING',
            max_length=50
        )
    ]

    address: Annotated[
        str, 
        Field(
            description="The training center's address",
            example='123 Fitness St, Muscle City, Fit State, 12345-678',
            max_length=200
        )
    ]

    property_name: Annotated[
        str,
        Field(
            description="The name of the property where the training center is located",
            example='Fitness Plaza',
            max_length=100
        )
    ]

class TrainingCenterPost(TrainingCenterBase):
    '''
    Schema for creating a new training center.
    '''
    pass
    

class TrainingCenterResponse(TrainingCenterPost, OutMixin):
    '''
    Schema for training center response data.
    '''
    pass

class TrainingCenterResponseWithAthletes(BaseSchema):
    '''
    Schema for training center response data including athletes.
    '''
    name: Annotated[
        str, 
        Field(
            description="The training center's full name",
            example='CT KING',
            max_length=50
        )
    ]