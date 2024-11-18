from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date
from typing import Optional


class SugerenciasValidator(BaseModel):
    NoSugerencia: int | None = None  # None = None Permite que sea opcional
    Titulo: str
    Descripcion: str
    Fecha: date
    Imagen: Optional[bytes] = None
