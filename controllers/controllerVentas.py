from datetime import date
from fastapi import Query
from typing import Annotated, List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from databaseConection.DBConecction import getDatabase
from services.AuthService import JWTAuthService
from models.schemas.schemaVentas import VentasValidator, VentasViewResponse
from services.ServiceVentas import VentasService

dbSession = Annotated[Session, Depends(getDatabase)]
tokenDependency = Depends(JWTAuthService.getCurrentUser)

ventRoute = APIRouter(prefix="/ventas", tags=["Ventas"])


@ventRoute.get("/",dependencies=[tokenDependency], response_model=List[VentasViewResponse])  
async def index(
    dbCon: dbSession,
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: dict = tokenDependency
):
    NoEmpleado = current_user.get("sub")  # Extrae el NoEmpleado del token
    response = VentasService.getAll(db=dbCon, start_date=start_date, end_date=end_date, NoEmpleado=NoEmpleado)
    
    if response:
        return response
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No existen registros en este rango de fechas")

