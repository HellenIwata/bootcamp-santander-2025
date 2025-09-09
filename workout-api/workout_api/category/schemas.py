'''
Schemas for category-related data.
'''

from datetime import datetime
from typing import Annotated

from pydantic import Field, UUID4

from workout_api.contrib.schemas import BaseSchema, OutMixin

class CategoryBase(BaseSchema):
    '''
    Base schema for category data.
    '''

    name: Annotated[
        str, 
        Field(
            description="The category's full name",
            example='Scaled',
            max_length=10
        )
    ]

    description: Annotated[
        str, 
        Field(
            description="A brief description of the category",
            example='Suitable for beginners with no prior experience.',
            max_length=200
        )
    ]

class CategoryPost(CategoryBase):
    '''
    Schema for creating a new category.
    '''
    pass

class CategoryResponse(CategoryPost, OutMixin):
    '''
    Schema for category response data.
    '''
    pass

class CategoryResponseWithAthletes(BaseSchema):
    '''
    Schema for category response data including athletes.
    '''
    name: Annotated[
        str, 
        Field(
            description="The category's full name",
            example='Scaled',
            max_length=10
        )
    ]