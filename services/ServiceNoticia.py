from sqlalchemy.orm import Session
from models.Models import Noticias
from models.schemas.schemaNoticia import NoticiaValidator
from typing import List
from sqlalchemy.orm import Session
from typing import Optional

"""
    Clase que proporciona métodos para gestionar operaciones relacionadas Noticias
    en la base de datos, incluyendo operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
    """


class NoticiaService:
    @classmethod
    def createNoticia(cls, noticias):
        return{
            "NoNoticias": noticias.NoNoticias,
            "Titulo": noticias.Titulo,
            "Descripcion": noticias.Descripcion,
            "Fecha": noticias.Fecha,
            "Imagen": noticias.Imagen
        }
    @classmethod
    def getAll(cls, db: Session) -> List[dict]:
        values = db.query(Noticias).all()
        return [NoticiaValidator(**noticias.__dict__).model_dump() for noticias in values if noticias]

    @classmethod
    def getById(cls, id: int, db: Session) -> NoticiaValidator:
        value = db.query(Noticias).get(id)
        if value:
            return cls.createNoticia(value)
        return None
    
    
    @classmethod
    def create(cls, noti: NoticiaValidator, Imagen: bytes, db: Session) -> bool:
        try:
            noticia = Noticias(
                Titulo=noti.Titulo,
                Descripcion=noti.Descripcion,
                Fecha=noti.Fecha,
                Imagen=Imagen  
            )
            db.add(noticia)
            db.commit()
            db.refresh(noticia)  # Refresca la instancia con los datos de la BD, por si se generó una clave primaria
            return True
        except Exception as ex:
            db.rollback()
            print(f"Error al crear la noticia: {ex}")
            return False
    
    @classmethod
    def update(cls, noti: NoticiaValidator, db: Session) -> bool:
        try:
            noticia = db.query(Noticias).get(noti.NoNoticias)
            if noticia:
                noticia.Titulo = noti.Titulo
                noticia.Descripcion = noti.Descripcion
                noticia.Fecha = noti.Fecha
                if noti.Imagen:
                    noticia.Imagen = noti.Imagen
                db.commit()
                db.refresh(noticia)
                return True
            return False  # Si no se encuentra la noticia
        except Exception as ex:
            db.rollback()
            print(ex)
            return False
            
    @classmethod
    def delete(cls, NoNoticias:int, db:Session):
        try:
            value = db.query(Noticias).get(NoNoticias)
            if value is not None:
                db.delete(value)
                db.commit()
                return True
        except Exception as ex: 
            db.rollback()
            print(ex)
        return False
