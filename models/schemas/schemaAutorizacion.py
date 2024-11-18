from pydantic import BaseModel

class EmpAutorizado(BaseModel): #establece el esquema a recibir en el login 
    """Modelo de datos para la autorización de empleados durante el proceso de inicio de sesión.
    
    Este modelo define el esquema que se espera recibir al realizar una solicitud de
    inicio de sesión (login). Asegura que los datos proporcionados cumplan con los
    tipos y formatos requeridos, facilitando la validación y gestión de la información
    de inicio de sesión de un empleado.
    """
    NoEmpleado:str
    PasswordEmp: str