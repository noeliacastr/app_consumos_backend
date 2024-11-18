import base64
from typing import Annotated, Optional
from datetime import date
from fastapi import Depends, APIRouter, HTTPException, status, File, UploadFile, Form 
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databaseConection.DBConecction import getDatabase
from models.schemas.schemaNoticia import NoticiaValidator
from services.ServiceNoticia import NoticiaService
from services.AuthService import JWTAuthService


dbSession = Annotated[Session, Depends(getDatabase)]
tokenDependency = Depends(JWTAuthService.getCurrentUser) 

notiRoute = APIRouter(prefix="/noticias", tags=["Noticias"])

def encode_image_to_base64(image_data: bytes) -> str:
    if image_data:
        return base64.b64encode(image_data).decode("utf-8")
    return None

@notiRoute.get("/",dependencies=[tokenDependency], status_code=status.HTTP_200_OK)
async def index(db: Session = Depends(getDatabase)):
    try:
        noticias = NoticiaService.getAll(db=db)
        for noticia in noticias:
            if noticia['Imagen']:
                noticia['Imagen'] = encode_image_to_base64(noticia['Imagen'])
        return noticias
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las noticias: {ex}"
        )

@notiRoute.get("/{id}",dependencies=[tokenDependency], status_code=status.HTTP_200_OK)
async def getNoticiaByIid(id: int, db: Session = Depends(getDatabase)):
    try:
        noticia = NoticiaService.getById(id=id, db=db)
        if noticia:
            if noticia['Imagen']:
                noticia['Imagen'] = encode_image_to_base64(noticia['Imagen'])
            return noticia
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la noticia con el ID {id}"
            )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la noticia: {ex}"
        )

@notiRoute.post("/", dependencies=[tokenDependency])
async def createNoticia(
    Titulo: str = Form(...),
    Descripcion: str = Form(...),
    Fecha: date = Form(...),
    Imagen: UploadFile = File(...),  # Imagen obligatoria
    db: Session = Depends(getDatabase)
):
    try:
        # Leer el contenido de la imagen
        imagen_data = await Imagen.read()

        # Asegurarte de que la imagen se leyó correctamente
        if not imagen_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionó una imagen válida o está vacía"
            )

        # Crear el objeto de validación NoticiaValidator con los datos
        noticia_data = NoticiaValidator(
            Titulo=Titulo,
            Descripcion=Descripcion,
            Fecha=Fecha,
            Imagen=imagen_data  # Asegúrate de que no es None
        )

        # Llamar al servicio de creación
        success = NoticiaService.create(noti=noticia_data, Imagen=imagen_data, db=db)
        if success:
            return {"message": "Noticia creada exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la noticia"
            )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la solicitud: {ex}"
        )

@notiRoute.put("/{NoNoticias}",dependencies=[tokenDependency], status_code=status.HTTP_200_OK)
async def updateNoticia(
    NoNoticias: int,
    Titulo: str = Form(...),
    Descripcion: str = Form(...),
    Fecha: date = Form(...),
    Imagen: UploadFile = File(None),  # Permitir que Imagen sea opcional
    db: Session = Depends(getDatabase)
):
    try:
        imagen_data = None
        if Imagen:
            imagen_data = await Imagen.read()
        noticia_data = NoticiaValidator(
            NoNoticias=NoNoticias,
            Titulo=Titulo,
            Descripcion=Descripcion,
            Fecha=Fecha,
            Imagen=imagen_data  # Puede ser None si no se actualiza la imagen
        )
        # Llamar al servicio de actualización
        success = NoticiaService.update(noti=noticia_data, db=db)
        if success:
            return {"message": "Noticia actualizada exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la noticia con el ID {NoNoticias} para actualizar"
            )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la noticia: {ex}"
        )
    

@notiRoute.delete("/{NoNoticias}", dependencies=[tokenDependency])
async def deleteNoticia(NoNoticias: int, dbCon: dbSession):
    if NoticiaService.delete(NoNoticias=NoNoticias, db=dbCon):
        return JSONResponse("Noticia eliminada exitosamente", status.HTTP_202_ACCEPTED)
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Error al eliminar la noticia: {NoNoticias} ")
    
    
