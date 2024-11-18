from pydantic import BaseModel, field_validator
from typing import Optional



class MenuValidator(BaseModel):
    NoMenu: int | None = None # None = None Permite que sea opcional
    Nombre: str
    Descripcion: str 
    Imagen: Optional[bytes] = None
    Categoria: str 
