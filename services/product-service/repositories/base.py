from typing import Any, Generic, Type, TypeVar, Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: Any) -> Optional[ModelType]:
        result = await self.session.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await self.session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: CreateSchemaType | Dict[str, Any]) -> ModelType:
        obj_in_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, *, db_obj: ModelType, obj_in: UpdateSchemaType | Dict[str, Any]) -> ModelType:
        obj_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, *, id: Any) -> ModelType:
        db_obj = await self.get(id=id)
        if db_obj:
            await self.session.delete(db_obj)
            await self.session.flush()
        return db_obj
