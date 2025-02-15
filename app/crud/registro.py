from app.crud.base import CRUDBase
from app.models.registro import Registro
from app.schemas.registro import RegistroCreate, RegistroUpdate


class CRUDRegistro(CRUDBase[Registro, RegistroCreate, RegistroUpdate]):
    """
    CRUD especifico para el modelo registro
    Herede de CRUDBase, permite agregar metodos personalizados
    """


registro_crud = CRUDRegistro(Registro)
