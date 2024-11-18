from models.Models import Sugerencias
from models.schemas.schemaSugerencias import SugerenciasValidator
from typing import List
from sqlalchemy.orm import Session
from databaseConection.DBConecction import SessionLocal
from typing import Optional


"""
    Clase que proporciona métodos para gestionar operaciones relacionadas con Sugerencias
    en la base de datos, incluyendo operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
    """

class SugerenciasSevice:
    @classmethod
    def createSugerencia(cls, sugerencia):
        return {
            "NoSugerencia": sugerencia.NoSugerencia,
            "Titulo": sugerencia.Titulo,
            "Descripcion": sugerencia.Descripcion,
            "Fecha": sugerencia.Fecha,
            # "NoEmpleado": sugerencia.NoEmpleado,
            # "nombreEmpleado": sugerencia.empleado.nombre if sugerencia.empleado else None,
            "Imagen": sugerencia.Imagen
        }
    
    @classmethod
    def getAll(cls, db: Session) -> List[dict]:
        values = db.query(Sugerencias).all()
        return [SugerenciasValidator(**sugerencias.__dict__).model_dump() for sugerencias in values]
    
    @classmethod
    def getById(cls, id: int, db: Session) -> SugerenciasValidator:
        value = db.query(Sugerencias).get(id)
        if value:
            return cls.createSugerencia(value)
        return None
    

    # @classmethod
    # def getAll(cls, db):
    #     values = db.query(Sugerencias).all()
    #     SugerenciaView = [cls.createSugerencia(sugerencias) for sugerencias in values]
    #     return SugerenciaView
    


    # @classmethod
    # def getById(cls, id: int, db: Session) -> SugerenciaView:
    #     value = db.query(Sugerencias).get(id)
    #     if value:
    #         return cls.createSugerencia(value)
    #     return None




    @classmethod
    def create(cls, suge: SugerenciasValidator, imagen: Optional[bytes], db: Session) -> bool:
        try:
            sugerencia = Sugerencias(
                Titulo=suge.Titulo,
                Descripcion=suge.Descripcion,
                Fecha=suge.Fecha,
                # NoEmpleado=suge.NoEmpleado, 
                Imagen=imagen if imagen else None 
            )
            db.add(sugerencia)
            db.commit()
            db.refresh(sugerencia)
            return True
        except Exception as exception:
            db.rollback()
            print(f"Error al crear la sugerencia: {exception}")
            return False

    @classmethod
    def update(cls, sugerencias: SugerenciasValidator, db: Session) -> bool:
        
        try:
            sug = db.query(Sugerencias).get(sugerencias.NoSugerencia)
            if sug:
                sug.Titulo = sugerencias.Titulo
                sug.Descripcion = sugerencias.Descripcion
                sug.Fecha = sugerencias.Fecha
                if sugerencias.Imagen is not None:
                    sugerencias.Imagen = sugerencias.Imagen
                db.commit()
                db.refresh(sug)
                return True
            return False
        except Exception as ex:
            db.rollback()
            print(ex)
            return False
        


    @classmethod
    def delete(cls, NoSugerencia:int, db:Session):
        try:
            value = db.query(Sugerencias).get(NoSugerencia)
            if value is not None:
                db.delete(value)
                db.commit()
                return True
        except Exception as ex: 
            db.rollback()
            print(ex)
        return False
        

