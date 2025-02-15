from typing import Type, TypeVar, Generic, Optional
from sqlmodel import Session, select, SQLModel
from pydantic import BaseModel

# Tipos genericos para modelos y esquemas
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Inicializa el CRUD con el modelo especifico
        """
        self.model = model

    def create(self, session: Session, obj_in: CreateSchemaType) -> ModelType:
        """
        Crea un nuevo registro en la base de datos
        """
        db_obj = self.model(**obj_in.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get(self, session: Session, id: int) -> Optional[ModelType]:
        """
        Obtiene un registro por su ID
        """
        return session.get(self.model, id)

    def get_all(
        self, session: Session, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """
        Obtiene todos los registros con paginacion
        """
        return session.exec(select(self.model).offset(skip).limit(limit)).all()

    def update(
        self, session: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Actualiza un registro existente
        """
        obj_data = obj_in.model_dump(
            exclude_unset=True
        )  # Solo los campos que proporcionados
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def delete(self, session: Session, id: int) -> Optional[ModelType]:
        """
        Elimina un registro por su ID
        """
        db_obj = session.get(self.model, id)
        if db_obj:
            session.delete(db_obj)
            session.commit()
        return db_obj
