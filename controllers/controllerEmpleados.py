from typing import Annotated, List
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databaseConection.DBConecction import getDatabase
from models.schemas.schemaAutorizacion import EmpAutorizado
from models.schemas.schemaEmpleados import EmpleadosValidator, UpdateEmp, EmpleadosViewResponse
from services.ServiceEmpleados import EmpleadosService
from  services.AuthService import JWTAuthService

dbSession = Annotated[Session, Depends(getDatabase)]
tokenDependency = Depends(JWTAuthService.getCurrentUser)

empRoute = APIRouter(prefix="/empleados", tags=["Empleados"])

@empRoute.get("/",  response_model=List[EmpleadosViewResponse])  # Cambiado a EmpleadosViewResponse
async def index(dbCon: dbSession):
    response = EmpleadosService.getAll(db=dbCon)
    if response: 
        return response
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No existen registros")
    
@empRoute.get("/{NoEmpleado}",  response_model=EmpleadosViewResponse)  # Cambiado a NoEmpleado y EmpleadosViewResponse
async def getByNoEmpleado(NoEmpleado: str, dbCon: dbSession) -> EmpleadosViewResponse:
    response = EmpleadosService.getByNoEmpleado(NoEmpleado=NoEmpleado, db=dbCon)
    if response: 
        return response
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"No existe un empleado con el NoEmpleado: {NoEmpleado}")


@empRoute.post("/", dependencies=[tokenDependency])
async def createEmp(emp: EmpleadosValidator, dbCon: dbSession):
    if EmpleadosService.existId(emp.NoEmpleado, db=dbCon):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "El usuario ya existe")
    
    if EmpleadosService.createEmp(empleados=emp, db=dbCon):
        return JSONResponse({"message": "Usuario creado exitosamente!"}, status.HTTP_200_OK)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error al registrar el usuario")

@empRoute.put("/{no_empleado:str}", response_model=EmpleadosViewResponse)
async def updateEmp(no_empleado: str, emp: UpdateEmp, dbCon: dbSession):
    if not EmpleadosService.updateEmp(no_empleado=no_empleado, update_data=emp, db=dbCon):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No existe un empleado con el NoEmpleado: {no_empleado}")
    
    updated_emp = EmpleadosService.getByNoEmpleado(NoEmpleado=no_empleado, db=dbCon)
    return updated_emp


@empRoute.post("/login", name="login")
async def logginForAccessToken(credentials: EmpAutorizado, dbCon: dbSession) -> str:
    user = JWTAuthService.authenticateUser(credentials.NoEmpleado, credentials.PasswordEmp, dbCon)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    accessToken = JWTAuthService.createAccessToken(data={
        "sub": str(user.NoEmpleado), 
        "Nombre": user.Nombre, 
        "Rol": user.Rol})
    return accessToken

@empRoute.get("/active/user", dependencies=[tokenDependency])
async def get_current_user(current = tokenDependency):
    if current: 
        print(current)
        return JSONResponse(content=current, status_code=200)
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authorized")