from models.Models import Ventas
from sqlalchemy.orm import Session, joinedload
from datetime import date
from models.schemas.schemaVentas import VentasValidator, VentasViewResponse
from typing import List



class VentasService:
    @classmethod 
    def getAll(cls, db: Session, start_date: date, end_date: date, NoEmpleado: str) -> List[VentasViewResponse]:
        ventas = (
            db.query(Ventas)
            .filter(
                Ventas.Fecha.between(start_date, end_date),
                Ventas.NoEmpleado == NoEmpleado  # Filtra por el NoEmpleado autenticado
            )
            .options(joinedload(Ventas.empleado))  # Carga la relación con Empleados
            .all()
        )
        return [
            VentasViewResponse(
                Fecha=venta.Fecha,
                Hora=venta.Hora,
                NoTicket=venta.NoTicket,
                Codigo=venta.Codigo,
                Costo=venta.Costo,
                Planilla=venta.Planilla,
                Descripcion=venta.Descripcion,
                NoEmpleado=venta.empleado.NoEmpleado if venta.empleado else None
            )
            for venta in ventas
        ]
    


