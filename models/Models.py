from typing import List
from sqlalchemy import Integer, String, Float, Date, NCHAR, ForeignKey, VARBINARY, Boolean, SmallInteger, BOOLEAN
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from databaseConection.DBConecction import Base

# en este apartado se debe de poner todos los atributos que tiene en la tabla de la base de datos, 
# aunque no se use todos pero se debe de ponery principalmente se pone la clave primaria de cada tabla 
# en def __init__(self, **kwargs): pone los atributos que quieres usar 


class Empleados(Base):
    # Modelo que representa a los empleados en el sistema, incluyendo información personal y credenciales.

    __tablename__= "Empleados"
    IdEmpleado: Mapped[int] = mapped_column(Integer, primary_key=True) # Clave primaria con identidad

    NoEmpleado: Mapped[str] = mapped_column(String(40))
    BadgeID: Mapped[str] = mapped_column(String(40))
    Nombre: Mapped[str] = mapped_column(String(140))
    Empresa: Mapped[str] = mapped_column(String(60), nullable=True)
    Departamento: Mapped[str] = mapped_column(String(60), nullable=True)
    Imagen: Mapped[str] = mapped_column(String(200), nullable=True)
    Subsidio: Mapped[bool] = mapped_column(Boolean, nullable=True)
    Cantidad: Mapped[int] = mapped_column(Integer, nullable=True)
    Auto: Mapped[bool] = mapped_column(Boolean, nullable=True)
    Fecha: Mapped[str] = mapped_column(String(40), nullable=True)
    Planta: Mapped[str] = mapped_column(String(60), nullable=True)
    TipoPago: Mapped[str] = mapped_column(String(60), nullable=True)
    CentroCostos: Mapped[str] = mapped_column(String(60), nullable=True)
    PasswordEmp: Mapped[str] = mapped_column(String(100))
    Estado: Mapped[bool] = mapped_column(Boolean, nullable=True)
    TipoSubsidio: Mapped[int] = mapped_column(Integer, nullable=True)
    DesbloqueoSub: Mapped[int] = mapped_column(Integer, nullable=True)
    SubAct: Mapped[bool] = mapped_column(Boolean, nullable=True)
    EstadoEmp: Mapped[bool] = mapped_column(Boolean, nullable=True)
    Rol: Mapped[str] = mapped_column(String(50), nullable=True)
    ventas = relationship("Ventas", back_populates="empleado")  # Relación con Ventas

    # Inicializa un nuevo empleado con los parámetros dados.
    def __init__(self, **kwargs):
        self.IdEmpleado = kwargs.get("IdEmpleado")
        self.NoEmpleado = kwargs.get("NoEmpleado")
        self.Nombre = kwargs.get("Nombre")
        self.Rol = kwargs.get("Rol")
        self.PasswordEmp = kwargs.get("PasswordEmp")



class Sugerencias(Base):  
    # Modelo que representa las sugerencias realizadas por los empleados, permitiendo registrar sus ideas y opiniones.
    __tablename__ = "Sugerencias"
    NoSugerencia: Mapped[int] = mapped_column(Integer, primary_key=True) # Clave primaria con identidad

    Titulo: Mapped[str] = mapped_column(String(200))  
    Descripcion: Mapped[str] = mapped_column(String)  
    Fecha: Mapped[Date] = mapped_column(Date)
    Imagen: Mapped[bytes] = mapped_column(VARBINARY, nullable=True)

    def __init__(self, **kwargs):
        self.NoSugerencia = kwargs.get("NoSugerencia")
        # self.NoEmpleado = kwargs.get("NoEmpleado")
        self.Titulo = kwargs.get("Titulo")
        self.Descripcion = kwargs.get("Descripcion")
        self.Fecha = kwargs.get("Fecha")
        self.Imagen = kwargs.get("Imagen")

class Menu(Base):
    __tablename__="Menu"
    NoMenu:Mapped[int] = mapped_column(Integer,primary_key=True) # Clave primaria con identidad

    Nombre:Mapped[str] = mapped_column(String(100))
    Descripcion:Mapped[str] = mapped_column(String)
    Imagen: Mapped[bytes] = mapped_column(VARBINARY, nullable=True)
    Categoria:Mapped[str] = mapped_column(String(100))

    def __init__(self, **kwargs):
        self.NoMenu = kwargs.get("NoMenu")
        self.Nombre = kwargs.get("Nombre")
        self.Descripcion = kwargs.get("Descripcion")
        self.Imagen = kwargs.get("Imagen")
        self.Categoria = kwargs.get("Categoria")

class Noticias(Base):
    __tablename__="Noticias"
    NoNoticias:Mapped[int] = mapped_column(Integer,primary_key=True) # Clave primaria con identidad

    Titulo:Mapped[str] = mapped_column(String(200))
    Descripcion:Mapped[str] = mapped_column(String)
    Fecha:Mapped[Date] = mapped_column(Date)
    Imagen: Mapped[bytes] = mapped_column(VARBINARY, nullable=False)

    def __init__(self, **kwargs):
        self.NoNoticias = kwargs.get("NoNoticias")
        self.Titulo = kwargs.get("Titulo")
        self.Descripcion = kwargs.get("Descripcion")
        self.Fecha = kwargs.get("Fecha")
        self.Imagen = kwargs.get("Imagen")


class Ventas(Base):
    __tablename__ = "Ventas"
    id_ventas: Mapped[int] = mapped_column(Integer, primary_key=True)# Clave primaria con identidad
    
    Fecha: Mapped[Date] = mapped_column(Date, nullable=False)
    Hora: Mapped[str] = mapped_column(String(40), nullable=True)
    NoTicket: Mapped[str] = mapped_column(String(30), nullable=True)
    NoEmpleado: Mapped[str] = mapped_column(String(40), nullable=True)
    Codigo: Mapped[str] = mapped_column(String(40), nullable=True)
    Costo: Mapped[float] = mapped_column(Float, nullable=True)
    Estado: Mapped[bool] = mapped_column(Boolean, nullable=True)
    Cantidad: Mapped[int] = mapped_column(SmallInteger, nullable=True)
    Operador: Mapped[str] = mapped_column(String(60), nullable=True)
    Impuesto: Mapped[float] = mapped_column(Float, nullable=True)
    SubsidioTotal: Mapped[float] = mapped_column(Float, nullable=True)
    Efectivo: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    SubPro: Mapped[bool] = mapped_column(Boolean, nullable=True)
    Prepago: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    Tarjeta: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    Envio_App: Mapped[int] = mapped_column(SmallInteger, nullable=True)
    Detalle_Envio: Mapped[str] = mapped_column(NCHAR(120), nullable=True)
    Descripcion: Mapped[str] = mapped_column(String, nullable=True)
    Planilla: Mapped[float] = mapped_column(Float)  # Este es el campo Planilla

    # Claves foráneas (ajustadas)
    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey('Productos.id_productos'), nullable=True)
    planilla_subsidio: Mapped[int] = mapped_column(Integer, ForeignKey('Subsidio.id_subsidio'), nullable=True)
    NoEmpleado: Mapped[str] = mapped_column(String(40), ForeignKey("Empleados.NoEmpleado"))
    # Relaciones
    producto: Mapped["Productos"] = relationship("Productos", back_populates="ventas")
    subsidios: Mapped["Subsidio"] = relationship("Subsidio", back_populates="ventas")
    empleado = relationship("Empleados", back_populates="ventas")

    def __init__(self, **kwargs):
        self.id_ventas = kwargs.get("id_ventas")
        self.Fecha = kwargs.get("Fecha")
        self.Hora = kwargs.get("Hora")
        self.NoTicket = kwargs.get("NoTicket")
        self.Codigo = kwargs.get("Codigo")
        self.Costo = kwargs.get("Costo")
        self.Planilla = kwargs.get("Planilla")  # Corregido de 'Plantilla' a 'Planilla'
        self.Descripcion = kwargs.get("Descripcion")
        self.NoEmpleado = kwargs.get("NoEmpleado")


class Subsidio(Base):
    __tablename__ = "Subsidio"
    
    id_subsidio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)# Clave primaria con identidad
    
    Semana: Mapped[str] = mapped_column(String(50))
    Cargo: Mapped[str] = mapped_column(String(50))
    NoEmpleado: Mapped[str] = mapped_column(String(40))
    NoTicket: Mapped[str] = mapped_column(String(30))
    Fecha: Mapped[Date] = mapped_column(Date)
    Hora: Mapped[str] = mapped_column(String(40))
    Operador: Mapped[str] = mapped_column(String(60))
    Descuento: Mapped[float] = mapped_column(Float)
    Planilla: Mapped[float] = mapped_column(Float)  # Campo relacionado con Ventas
    Impuesto: Mapped[float] = mapped_column(Float)
    Site: Mapped[str] = mapped_column(String(50))
    Efectivo: Mapped[float] = mapped_column(DECIMAL(10, 2))
    Envio_Hacienda: Mapped[str] = mapped_column(String(50))
    Clave_Numerica: Mapped[str] = mapped_column(String(50))
    Detalle_Envio: Mapped[str] = mapped_column(String(120))
    Num_Carga: Mapped[str] = mapped_column(String(50))
    Prepago: Mapped[float] = mapped_column(DECIMAL(10, 2))
    Tarjeta: Mapped[float] = mapped_column(DECIMAL(10, 2))
    
    # Relación inversa con Ventas
    ventas: Mapped[List["Ventas"]] = relationship("Ventas", back_populates="subsidios")

    def __init__(self, **kwargs):
        self.id_subsidio = kwargs.get("id_subsidio")
        self.Planilla = kwargs.get("Planilla")


class Productos(Base):
    __tablename__ = "Productos"
    
    id_productos: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) # Clave primaria con identidad

    Codigo: Mapped[str] = mapped_column(String(40))
    Descripcion: Mapped[str] = mapped_column(String)  # NVARCHAR(MAX) como String
    Costo: Mapped[float] = mapped_column(Float)
    Proveedor: Mapped[str] = mapped_column(String(50))
    CCompra: Mapped[str] = mapped_column(String(50))
    Iva: Mapped[float] = mapped_column(Float)
    SubPro: Mapped[bool] = mapped_column(Boolean)  # BIT como BOOLEAN
    Empresa: Mapped[str] = mapped_column(String(50))
    codigo_cabys: Mapped[str] = mapped_column(String(50))

    # Relación inversa con Ventas
    ventas: Mapped[List["Ventas"]] = relationship("Ventas", back_populates="producto")

    def __init__(self, **kwargs):
        self.id_productos = kwargs.get("id_productos")
        self.Descripcion = kwargs.get("Descripcion")
        self.Codigo = kwargs.get("Codigo")
        



