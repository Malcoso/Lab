from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Producto, Venta
from ventas import altaventa, ventasgen, busquedaventa, modificarventa, borrarventa
from schema import VentaCrear, VentaRespuesta

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.post("", response_model=VentaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_venta(datos: VentaCrear, db: Session = Depends(get_db)):
    producto = db.get(Producto, datos.producto_id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado. No se puede realizar la venta.")

    if datos.cantidad <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cantidad debe ser mayor que cero.")

    venta = Venta(
        dia=datos.dia_venta,
        hora=datos.hora_venta,
        producto_id=datos.producto_id,
        cantidad=datos.cantidad,
        precio_total=producto.precio * datos.cantidad,
    )
    altaventa(venta, db)
    return venta


@router.get("/", response_model=list[VentaRespuesta])
def listar_ventas(db: Session = Depends(get_db)):
    return ventasgen(db)


@router.get("/{id}", response_model=VentaRespuesta)
def obtener_venta(id: int, db: Session = Depends(get_db)):
    venta = busquedaventa(id, db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")
    return venta


@router.put("/{id}", response_model=VentaRespuesta)
def modificar_venta(id: int, datos: VentaCrear, db: Session = Depends(get_db)):
    venta = db.get(Venta, id)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    producto = db.get(Producto, datos.producto_id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado. No se puede modificar la venta.")

    if datos.cantidad <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cantidad debe ser mayor que cero.")

    modificarventa(venta, datos, db)
    return venta


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(id: int, db: Session = Depends(get_db)):
    venta = db.get(Venta, id)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    borrarventa(venta, db)
    return {"detail": "Venta eliminada."}
