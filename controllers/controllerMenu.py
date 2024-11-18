import base64
from typing import Optional, Annotated
from fastapi import Depends, APIRouter, HTTPException, status, File, UploadFile, Form 
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databaseConection.DBConecction import getDatabase
from models.schemas.schemaMenu import MenuValidator
from services.ServiceMenu import MenuService
from services.AuthService import JWTAuthService


dbSession = Annotated[Session, Depends(getDatabase)]
tokenDependency = Depends(JWTAuthService.getCurrentUser) 

menuRoute = APIRouter(prefix="/menu", tags=["Menu"])


def encode_image_to_base64(image_data: bytes) -> str:
    if image_data:
        return base64.b64encode(image_data).decode("utf-8")
    return None

# Ruta para obtener todos los menús
@menuRoute.get("/", dependencies=[tokenDependency],  status_code=status.HTTP_200_OK)
async def index(db: Session = Depends(getDatabase)):
    try:
        menus = MenuService.getAll(db=db)
        for menu in menus:
            if menu['Imagen']:
                menu['Imagen'] = encode_image_to_base64(menu['Imagen'])
        return menus
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los menús: {ex}"
        )
# Ruta para obtener un menú por su ID
@menuRoute.get("/{NoMenu}", dependencies=[tokenDependency], status_code=status.HTTP_200_OK)
async def getMenuByIid(NoMenu: int, db: Session = Depends(getDatabase)):
    try:
        menu = MenuService.getById(NoMenu=NoMenu, db=db)  # Cambiar 'id' a 'NoMenu'
        if menu:
            if menu['Imagen']:  # Cambiar 'menu.imagen' a 'menu['imagen']' porque 'menu' es un diccionario
                menu['Imagen'] = encode_image_to_base64(menu['Imagen'])
            return menu
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el menú con el número {NoMenu}"
            )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el menú: {ex}"
        )


@menuRoute.post("/", dependencies=[tokenDependency])
async def createMenu(
    Nombre: str = Form(...),
    Descripcion: str = Form(...),
    Imagen: Optional[UploadFile] = File(None),
    Categoria: str = Form(...),
    db: Session = Depends(getDatabase)
):
    try:
        imagen_data = None
        if Imagen:
            imagen_data = await Imagen.read()
        menu_data = MenuValidator(
            Nombre=Nombre,
            Descripcion=Descripcion,
            Categoria=Categoria
        )
        success = MenuService.create(men=menu_data, imagen=imagen_data, db=db)
        if success:
            return {"message": "Menú creada exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la menú"
            )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la solicitud: {ex}"
        )
    

@menuRoute.put("/{NoMenu}", dependencies=[tokenDependency], status_code=status.HTTP_200_OK)
async def updateNoticia(
    NoMenu: int,
    Nombre: str = Form(...),
    Descripcion: str = Form(...),
    Imagen: Optional[UploadFile] = File(None),
    Categoria: str = Form(...), 
    db: Session = Depends(getDatabase)
):
    try:
        imagen_data = None
        if Imagen:
            imagen_data = await Imagen.read()
        menu_data = MenuValidator(
            NoMenu=NoMenu,
            Nombre=Nombre,
            Descripcion=Descripcion,
            Categoria=Categoria,
            Imagen=imagen_data  # Puede ser None si no se actualiza la imagen
        )
        # Llamar al servicio de actualización
        success = MenuService.update(men=menu_data, db=db)
        if success:
            return {"message": "Menú actualizada exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el menú con el número {NoMenu} para actualizar"
            )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el menú: {ex}"
        )
    
@menuRoute.delete("/{NoMenu}", dependencies=[tokenDependency])
async def deleteMenu(NoMenu: int, dbCon: dbSession):
    if MenuService.delete(NoMenu=NoMenu, db=dbCon):
        return JSONResponse("Menu eliminada exitosamente", status.HTTP_202_ACCEPTED)
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Error al eliminar la noticia: {NoMenu} ")
    
    

    
