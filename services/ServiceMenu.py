from sqlalchemy.orm import Session
from typing import List, Optional
from models.Models import Menu
from models.schemas.schemaMenu import MenuValidator

"""
    Clase que proporciona métodos para gestionar operaciones relacionadas Menu
    en la base de datos, incluyendo operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
    """

class MenuService:
    @classmethod
    def createMenu(cls, menu):
        return {
            "NoMenu": menu.NoMenu,
            "Nombre": menu.Nombre,
            "Descripcion": menu.Descripcion,
            "Imagen": menu.Imagen,
            "Categoria": menu.Categoria,
        }

    @classmethod
    def getAll(cls, db: Session) -> List[dict]:
        values = db.query(Menu).all()
        return [cls.createMenu(menu) for menu in values]  
    
    @classmethod
    def getById(cls, NoMenu: int, db: Session) -> Optional[dict]:
        value = db.query(Menu).get(NoMenu)
        if value:
            return cls.createMenu(value)
        return None

    @classmethod
    def create(cls, men: MenuValidator, imagen: Optional[bytes], db: Session) -> bool:
        try:
            menu = Menu(
                Nombre=men.Nombre,
                Descripcion=men.Descripcion,
                Categoria=men.Categoria,
                Imagen=imagen if imagen else None
            )
            db.add(menu)
            db.commit()
            db.refresh(menu)
            return True
        except Exception as ex:
            db.rollback()
            print(f"Error al crear el menú: {ex}")
            return False
        
    @classmethod
    def update(cls, men: MenuValidator, db: Session) -> bool:
        try:
            menu = db.query(Menu).get(men.NoMenu)
            if menu:
                menu.Nombre = men.Nombre
                menu.Descripcion = men.Descripcion
                menu.Categoria = men.Categoria
                if men.Imagen is not None:
                    menu.Imagen = men.Imagen
                db.commit()
                db.refresh(menu)
                return True
            return False
        except Exception as ex:
            db.rollback()
            print(ex)
            return False
        
    @classmethod
    def delete(cls, NoMenu: int, db: Session) -> bool:
        try:
            value = db.query(Menu).get(NoMenu)
            if value is not None:
                db.delete(value)
                db.commit()
                return True
        except Exception as ex: 
            db.rollback()
            print(ex)
        return False
