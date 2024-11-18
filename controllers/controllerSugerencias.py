
import base64
from typing import Annotated, List, Optional
from datetime import date
from fastapi import Depends, APIRouter, HTTPException, status, File, UploadFile, Form 
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databaseConection.DBConecction import getDatabase
from models.schemas.schemaSugerencias import SugerenciasValidator
from services.ServiceSugerencia import SugerenciasSevice
from services.AuthService import JWTAuthService


dbSession = Annotated[Session, Depends(getDatabase)]
tokenDependency = Depends(JWTAuthService.getCurrentUser)

sugRoute = APIRouter(prefix="/sugerencias", tags=["Sugerencias"])

def encode_image_to_base64(image_data: bytes) -> str:
    if image_data:
        return base64.b64encode(image_data).decode("utf-8")
    return None



@sugRoute.get("/", dependencies=[tokenDependency], status_code=status.HTTP_200_OK)
async def index(db: Session = Depends(getDatabase)):
    try:
        sugerencias = SugerenciasSevice.getAll(db=db)
        for sugerencia in sugerencias:
            if sugerencia['Imagen']:
                sugerencia['Imagen'] = encode_image_to_base64(sugerencia['Imagen'])
        return sugerencias
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las sugerencias: {ex}"
        )

@sugRoute.get("/{id}",dependencies=[tokenDependency])
async def getSugeByIid(id: int, db: Session = Depends(getDatabase)):
    try:
        sugerencia = SugerenciasSevice.getById(id=id, db=db)
        if sugerencia:
            if sugerencia['Imagen']:
                sugerencia['Imagen'] = encode_image_to_base64(sugerencia['Imagen'])
            return sugerencia
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la Sugerencia con el número {id}"
            )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la sugerencia: {ex}"
        )


@sugRoute.post("/", dependencies=[tokenDependency])
async def createSuge(
    Titulo: str = Form(...),
    Descripcion: str = Form(...),
    Fecha: date = Form(...),
    # NoEmpleado: int = Form(...),
    Imagen: Optional[UploadFile] = File(None),  
    db: Session = Depends(getDatabase)
):
    try:
        imagen_data = None
        if Imagen:
            imagen_data = await Imagen.read()
        suge_data = SugerenciasValidator(
            Titulo=Titulo,
            Descripcion=Descripcion,
            Fecha=Fecha
            # NoEmpleado=NoEmpleado,
        )
        # Cambia Imagen a imagen para que coincida con el método create
        success = SugerenciasSevice.create(suge=suge_data, imagen=imagen_data, db=db)
        if success:
            return {"message": "Sugerencia creada exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la sugerencia en el servicio"
            )
    except Exception as ex:
        print(f"Error específico en el controlador: {ex}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la solicitud: {ex}"
        )
    


@sugRoute.put("/{NoSugerencia}", dependencies=[tokenDependency], status_code=status.HTTP_200_OK)
async def updateSugerencia(
    NoSugerencia: int,
    Titulo: str = Form(...),
    Descripcion: str = Form(...),
    Fecha: date = Form(...),
    Imagen: Optional[UploadFile] = File(None),
    db: Session = Depends(getDatabase)
):
    try:
        # Leer el contenido de la imagen si se proporciona
        imagen_data = None
        if Imagen:
            imagen_data = await Imagen.read()

        # Crear un objeto de validación SugerenciasValidator con los nuevos datos
        suge_data = SugerenciasValidator(
            NoSugerencia=NoSugerencia,
            Titulo=Titulo,
            Descripcion=Descripcion,
            Fecha=Fecha,
            Imagen=imagen_data  # Puede ser None si no se actualiza la imagen
        )

        # Llamar al servicio de actualización con el nombre correcto del argumento
        success = SugerenciasSevice.update(sugerencias=suge_data, db=db)
        if success:
            return {"message": "Sugerencia actualizada exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la sugerencia con el número {NoSugerencia} para actualizar"
            )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la sugerencia: {ex}"
        )
    
@sugRoute.delete("/{NoSugerencia}", dependencies=[tokenDependency])
async def deleteNoticia(NoSugerencia: int, dbCon: dbSession):
    if SugerenciasSevice.delete(NoSugerencia=NoSugerencia, db=dbCon):
        return JSONResponse("Sugerencia eliminada exitosamente", status.HTTP_202_ACCEPTED)
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Error al eliminar la Sugerencia: {NoSugerencia} ")