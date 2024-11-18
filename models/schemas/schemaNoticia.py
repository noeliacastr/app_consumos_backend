from pydantic import BaseModel, field_validator
from datetime import date
# from typing import Optional


class NoticiaValidator(BaseModel):
    NoNoticias: int | None = None  # None = None Permite que sea opcional
    Titulo: str
    Descripcion: str
    Fecha: date
    Imagen: bytes = None
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
        }

