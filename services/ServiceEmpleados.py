from models.Models import Empleados
from sqlalchemy.orm import Session  # Solo importa Session
from passlib.context import CryptContext
from models.schemas.schemaEmpleados import EmpleadosValidator, UpdateEmp, EmpleadosViewResponse
from typing import List

class EmpleadosService:

    """
    Clase que proporciona métodos para gestionar operaciones relacionadas con los empleados
    en la base de datos, incluyendo operaciones CRUD (Crear, Leer, Actualizar).
    """

    _context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod 
    def getAll(cls, db: Session) -> List[EmpleadosViewResponse]:  # Cambiar dbSession a Session
        empleados = db.query(Empleados).all()
        print(empleados)  
        return [
            EmpleadosViewResponse(
                NoEmpleado=empleado.NoEmpleado,
                Nombre=empleado.Nombre if empleado.Nombre is not None else "Sin nombre",
                Rol=empleado.Rol or "Desconocido",
            )
            for empleado in empleados
        ]
    

    @classmethod
    def updateEmp(cls, no_empleado: str, update_data: UpdateEmp, db: Session) -> bool:
        try:
            empleado = db.query(Empleados).filter(Empleados.NoEmpleado == no_empleado).first()
            if not empleado:
                return False
            
            # Actualiza los atributos del empleado con los datos proporcionados
            if update_data.Nombre is not None:
                empleado.Nombre = update_data.Nombre
            if update_data.Rol is not None:
                empleado.Rol = update_data.Rol
            if update_data.PasswordEmp is not None:
                empleado.PasswordEmp = cls._context.hash(update_data.PasswordEmp)
            
            db.commit()
            return True
        except Exception as ex:
            db.rollback()
            print(ex)
        return False

    @classmethod
    def getByNoEmpleado(cls, NoEmpleado: str, db: Session) -> EmpleadosViewResponse:
        value = db.query(Empleados).filter(Empleados.NoEmpleado == NoEmpleado).first()
        if value:
            return EmpleadosViewResponse(
                NoEmpleado=value.NoEmpleado,
                Nombre=value.Nombre,
                Rol=value.Rol
            )
        return None

    @classmethod
    def createEmp(cls, empleados: EmpleadosValidator, db: Session) -> bool:
        try:
            empleado = Empleados(**empleados.model_dump())
            empleado.PasswordEmp = cls._context.hash(empleado.PasswordEmp)
            db.add(empleado)
            db.commit()
            return True
        except Exception as ex: 
            db.rollback()
            print(ex)
        return False


# Verifica si existe un empleado con un número de empleado específico.
    @classmethod
    def existId(cls, id: int, db: Session) -> bool:
        try:
            empleadoExistente = db.query(Empleados).filter(Empleados.NoEmpleado == id).first()
            if empleadoExistente:
                if not empleadoExistente.user:
                    return True
                else:
                    return False
            return False
        except Exception as ex:
            db.rollback()
            print(ex)
        return False
