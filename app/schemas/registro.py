from datetime import date
from pydantic import BaseModel


class RegistroCreate(BaseModel):
    """
    Esquema de entrada de datos que el cliente envia
    """

    fecha: date
    tipo: str
    descripcion: str
    color: str


class RegistroRead(BaseModel):
    """
    Esquema de datos que la API envia al cliente
    """

    id: int
    fecha: date
    tipo: str
    descripcion: str
    color: str


class RegistroUpdate(BaseModel):
    """
    Esquema de datos que el cliente envia para actualizar un registro existente
    """

    fecha: date | None
    tipo: str | None
    descripcion: str | None
    color: str | None
