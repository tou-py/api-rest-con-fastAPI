from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.registro import Registro
from datetime import date


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombres: str
    apellidos: str
    email: str = Field(unique=True, index=True)
    hashed_password: str
    fecha_creacion: date

    # registros: List["Registro"] = Relationship(back_populates="usuario")
