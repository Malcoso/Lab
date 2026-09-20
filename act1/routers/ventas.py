from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Producto, Venta,Carrito_Producto
from ventas import altaventa, ventasgen, busquedaventa, modificarventa, borrarventa,obtener_venta,mostrarventa
from carrito import busquedacarrito
from schema import VentaCrear, VentaRespuesta,VentaListaRespuesta,VentaDetalleRespuesta

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_venta(datos: VentaCrear, db: Session = Depends(get_db)):
    carrito = busquedacarrito(datos.carrito_id,db)
    if carrito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")
    
    venta = Venta(
        dia=datos.dia_venta,
        hora=datos.hora_venta,
        carrito_id = datos.carrito_id
    )
    altaventa(venta, db)
    return {"detail":"Venta creada"}


@router.get("/", response_model=list[VentaListaRespuesta])
def listar_ventas(db: Session = Depends(get_db)):
    return ventasgen(db)


@router.get("/{id}", response_model=VentaDetalleRespuesta)
def obtener_venta(id: int, db: Session = Depends(get_db)):
    venta = busquedaventa(id, db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    carrito = busquedacarrito(venta.carrito_id, db)
    if carrito is None:
        raise HTTPException(status_code=404, detail="No existe el carrito")

    return mostrarventa(venta, db)


@router.put("/{id}", response_model=VentaDetalleRespuesta)
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

@router.post("/{id}/carrito",response_model = VentaRespuesta,status_code=status.HTTP_201_CREATED)
def enlazar_venta(
    id : int,
    carrito : int,
    db : Session=Depends(get_db)
):
    venta = obtener_venta(id,db)
    if venta is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")
    
    carritos = busquedacarrito(carrito,db)
    if carritos is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    dato = Venta(
        dia=venta.dia,
        hora=venta.hora,
        id_carrito=carrito
    )

    modificarventa(venta,dato,db)
    return dato




