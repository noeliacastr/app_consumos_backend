import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import Empleados

load_dotenv(".env")

class JWTAuthService:
    # Servicio de autenticación basado en JWT para gestionar el acceso de usuarios.
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/coral/empleados/login") 
    tokenDependency = Annotated[str, Depends(oauth2_scheme)]
    _context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

    @classmethod 
    def verifyPassword(cls, PasswordEmp, hashedPassword) -> bool: #metodo para verificar la contraseña
        return cls._context.verify(PasswordEmp, hashedPassword) #Verifica si la contraseña ingresada coincide con la contraseña hasheada.
    
    @classmethod
    def getPasswordHash(cls, PasswordEmp:str) -> str: #Devuelve la contraseña hasheada utilizando bcrypt.
        return cls._context.hash(PasswordEmp) 
    
    @classmethod
    def rehashPasswordIfNeeded(cls, empl: Empleados, db: Session) -> None:
        """
        Rehashea la contraseña del usuario si no está en el formato esperado.
        """
        if not empl.PasswordEmp.startswith("$2b$"):  # Verifica si el hash es un bcrypt
            empl.PasswordEmp = cls.getPasswordHash(empl.PasswordEmp)  # Rehashea la contraseña
            db.add(empl)
            db.commit()
    
    @classmethod
    def authenticateUser(cls, NoEmpleado:str, PasswordEmp:str, db:Session): #metodo para auteticar el usuario
        empl = db.query(Empleados).filter(Empleados.NoEmpleado == NoEmpleado).first() #consulta que busca el usuario por su número de empleado
        if not empl:
            return False 
        cls.rehashPasswordIfNeeded(empl, db)  # Rehashear la contraseña si es necesario
        if not cls.verifyPassword(PasswordEmp, empl.PasswordEmp): 
            return False 
        return empl  
    
    @classmethod
    def createAccessToken(cls, data): #metodo para crear token de acceso
        to_encode = data.copy() 
        expire = datetime.utcnow() + timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))) #minutos de expiracion del token
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
        return encoded_jwt
    
    @classmethod
    async def getCurrentUser(cls, token:tokenDependency) -> str: #metodo para obtener el usuario actual que esta logeado 
        try:
            payload = jwt.decode(token, key=os.getenv('SECRET_KEY'), algorithms=os.getenv('ALGORITHM'))
            print(payload)
            data = payload.get("sub")
            if data is None: 
                raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
            del payload["exp"]
            print(payload)
            return payload
        except JWTError as ex:
            print(ex)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
