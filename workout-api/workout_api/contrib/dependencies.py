from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from workout_api.configs.database import get_async_session

DatabaseDependency = Annotated[AsyncSession, Depends(get_async_session)]