from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date


class Registro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    tipo: str
    descripcion: str
    color: str

    # relacion con el usuario
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    # usuario: Optional[Usuario] = Relationship(back_populates="registros")

    def get_usuario(self):
        from app.models.usuario import Usuario

        return Usuario
