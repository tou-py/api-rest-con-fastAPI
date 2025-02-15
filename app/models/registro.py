from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class Registro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    tipo: str
    descripcion: str
    color: str
