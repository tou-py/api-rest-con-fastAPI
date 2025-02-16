from typing import Type, TypeVar, Generic, Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, SQLModel
from pydantic import BaseModel

# Tipos genéricos para modelos y esquemas
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Inicializa el CRUD con el modelo específico
        """
        self.model = model

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        """
        Crea un nuevo registro a partir de un modelo
        """
        db_objt = self.model(**obj_in.model_dump())
        session.add(db_objt)
        await session.commit()
        await session.refresh(db_objt)
        return db_objt

    async def get(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Obtiene un registro por su ID
        """
        return await session.get(self.model, id)

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Obtiene todos los registros con paginación.
        """
        result = await session.scalars(select(self.model).offset(skip).limit(limit))
        return result.all()  # Extrae y devuelve los objetos

    async def update(
        self, session: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Actualiza un registro existente
        """
        obj_data = obj_in.model_dump(
            exclude_unset=True
        )  # Solo los campos proporcionados
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Elimina un registro por su ID
        """
        db_obj = await session.get(self.model, id)
        if db_obj:
            await session.delete(db_obj)
            await session.commit()
        return db_obj
