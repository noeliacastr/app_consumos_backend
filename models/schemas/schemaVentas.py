from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date

class VentasValidator(BaseModel):
    """
    Modelo de validación para las ventas realizadas por los empleados.
    Este modelo se utiliza para validar y gestionar los datos relacionados con
    una transacción de venta, asegurando que se cumplan las reglas de formato
    y tipo de datos. Incluye campos opcionales y requiere ciertos datos 
    para la creación de una venta.
    """
    # Configuración para permitir la creación de modelos a partir de atributos de diccionario
    model_config = ConfigDict(from_attributes=True)
    id_ventas: int | None = None # Identificador único de la venta, puede ser None si no se especifica
    Fecha: date
    Hora: str
    NoTicket: str
    Codigo: Optional[str]
    Costo: float
    Planilla: Optional[float]
    Descripcion: Optional[str]
    NoEmpleado: Optional[str]

# -------------------------------------------------------------------------

class VentasViewResponse(BaseModel):
    """Modelo de respuesta para la vista de ventas.
    Este modelo se utiliza para estructurar la información que se devolverá
    cuando se consulte una venta, proporcionando un formato consistente para
    los datos de venta sin incluir el identificador de la venta.
    """
    Fecha: date
    Hora: str
    NoTicket: str
    Codigo: Optional[str]
    Costo: float
    Planilla: Optional[float]
    Descripcion: Optional[str]
    NoEmpleado: Optional[str]

