import datetime
from datetime import datetime
from typing import Annotated, Optional
from pydantic import UUID4, BaseModel, Field


class BaseSchema(BaseModel):

    '''
    Base schema for common fields.
    '''

    class Config:
        extra = 'forbid'
        from_attributes = True

class OutMixin(BaseSchema):
    id: Annotated[
        UUID4,
        Field(
            description ="The unique identifier",
            example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    ]
    created_at: Annotated[
        datetime,
        Field(
            description="The timestamp when the record was created",
            example="2023-10-05T14:48:00.000Z"
        )
    ]
    updated_at: Annotated[
        datetime,
        Field(
            description="The timestamp when the record was last updated",
            example="2023-10-10T10:20:30.000Z"
        )
    ]