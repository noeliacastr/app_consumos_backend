import os
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import router

# Carga las variables de entorno desde un archivo .env
load_dotenv()

# Se crea una instancia de la aplicación FastAPI
app = FastAPI()


# Lista de orígenes permitidos para las solicitudes CORS
origins = [
    "http://localhost", # Permite solicitudes desde localhost
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8000/coral/empleados",
    "http://127.0.0.1:8000/coral/empleado/login",
    "http://127.0.0.1:8000/coral/sugerencias",
    "http://127.0.0.1:8000/coral/noticias",
    "http://127.0.0.1:8000/coral/menu",
    "http://127.0.0.1:8000/coral/ventas"
]


# Configuración del middleware CORS para gestionar las solicitudes cruzadas
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Especifica los orígenes permitidos
    allow_credentials=True,   # Permite el uso de credenciales (como cookies)
    allow_methods=["*"],      # Permite todos los métodos HTTP
    allow_headers=["*"],      # Permite todos los encabezados
)


app.include_router(router=router, prefix="/coral") #ruta principal 


# Ejecuta la aplicación usando uvicorn si el script se ejecuta como programa principal
if __name__ == "__main__": 
    uvicorn.run(app)
