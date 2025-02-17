from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, TypeVar, Generic

U = TypeVar("U")


# Esquema de respuesta de la api
class APIResponse(BaseModel, Generic[U]):
    data: Optional[U] = None
    message: str
    status_code: int
    pagination: Optional[dict] = None


# Esquema para crear un usuario
class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr
    password: str  # en texto normal


# Esquema para leer un usuario
class UsuarioRead(BaseModel):
    id: int
    nombres: str
    apellidos: str
    email: EmailStr
    fecha_creacion: datetime


# Esquema para actualizar un usuario
class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
