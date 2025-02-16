from typing import Type, TypeVar, Generic, Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, SQLModel
from pydantic import BaseModel, ValidationError
from contextlib import asynccontextmanager

# Tipos genéricos para modelos y esquemas
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


@asynccontextmanager
async def get_transaction(session: AsyncSession):
    """
    Context manager que sirve para manejar transacciones
    """
    try:
        yield session
        await session.commit()
    except Exception as ex:
        await session.rollback()
        raise ex


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Inicializa el CRUD con el modelo específico
        """
        self.model = model

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

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        """
        Crea un nuevo registro a partir de un modelo
        """
        if not obj_in or not isinstance(obj_in, CreateSchemaType):
            raise ValueError("Datos no proporcionados")

        async with get_transaction(session):
            db_objt = self.model(**obj_in.model_dump())
            session.add(db_objt)
            await session.refresh(db_objt)
            return db_objt

    async def update(
        self, session: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Actualiza un registro existente
        """
        if not db_obj or not isinstance(obj_in, UpdateSchemaType):
            raise ValueError("El registro no existe o no posee la estructura correcta")

        async with get_transaction(session):
            obj_data = obj_in.model_dump(
                exclude_unset=True
            )  # Solo los campos proporcionados
            for key, value in obj_data.items():
                if not hasattr(db_obj, key):
                    raise ValueError(f"El campo '{key}' no existe en el modelo")
                setattr(db_obj, key, value)
            session.add(db_obj)
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
