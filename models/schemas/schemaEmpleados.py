from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class EmpleadosValidator(BaseModel):
    # """Modelo de validación para empleados.
    
    # Este modelo se utiliza para validar la información de un empleado,
    # incluyendo sus credenciales y detalles relevantes. Asegura que los
    # datos cumplan con los tipos y formatos requeridos al crear o actualizar
    # registros de empleados.
    # """
    # 
    model_config = ConfigDict(from_attributes=True)
    IdEmpleado: int | None = None # None = None Permite que sea opcional
    NoEmpleado: str | None = None
    Nombre: str
    Rol: str | None = None
    PasswordEmp: str 

# -------------------------------------------------------------------------

class EmpleadosViewResponse(BaseModel):
    # Modelo de respuesta para la visualización de datos de empleados.
    NoEmpleado: str | None = None
    Nombre: Optional[str]
    Rol: Optional[str]

# -------------------------------------------------------------------------

class UpdateEmp(BaseModel):
    IdEmpleado: int | None = None
    NoEmpleado: str | None = None
    Nombre: str | None = None
    Rol: str | None = None
    PasswordEmp: str | None = None
    

# -------------------------------------------------------------------------

def to_dict(self):
    # """Convierte la instancia de la clase en un diccionario.
    
    # Esta función devuelve un diccionario que contiene los atributos de 
    # la instancia, lo que facilita la manipulación y el envío de datos
    # en un formato estructurado.
    # """
    return{
        "IdEmpleado": self.IdEmpleado,
        "NoEmpleado": self.NoEmpleado,
        "Nombre": self.Nombre,
        "Rol": self.Rol,
        "PasswordEmp": self.PasswordEmp
    }