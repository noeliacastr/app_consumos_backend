from fastapi import APIRouter


# Importación de los controladores que manejarán las rutas de diferentes entidades
from controllers.controllerEmpleados import empRoute
from controllers.controllerSugerencias import sugRoute
from controllers.controllerNoticia import notiRoute
from controllers.controllerMenu import menuRoute
from controllers.controllerVentas import ventRoute

# Se crea una instancia de APIRouter para definir un conjunto de rutas.
router = APIRouter()

# Esto permite agrupar las rutas relacionadas y manejarlas de manera organizada.
router.include_router(router=empRoute)
router.include_router(router=sugRoute)
router.include_router(router=notiRoute)
router.include_router(router=menuRoute)
router.include_router(router=ventRoute)