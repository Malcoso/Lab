from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy.orm import Session

from database import get_db

from models import Venta
from ventas import altaventa, getcarritoventa, getdiaventa, gethoraventa, busquedaventa, modificarventa, borrarventa, mostrarventa, mostrarventasimple
from carrito import busquedacarrito,getidcarrito,getestadocarrito

from schema import VentaCrear,VentaListaRespuesta,VentaDetalleRespuesta

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_venta(datos: VentaCrear, db: Session = Depends(get_db)):
    carrito = busquedacarrito(datos.carrito_id, db)
    if carrito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")

    if (carrito.venta is not None) or (carrito.venta == 0):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este carrito ya esta asociado a una venta")

    venta = Venta(
        dia=datos.dia_venta,
        hora=datos.hora_venta,
        carrito_id=datos.carrito_id,
        precio_total=0.0
    )

    if busquedacarrito(venta.carrito_id, db) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")
    
    altaventa(venta, db)
    return {"detail": "Venta creada"}


@router.get("/", response_model=list[VentaListaRespuesta]) 
def listar_ventas(
    db: Session = Depends(get_db),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
):
    query = db.query(Venta)

    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser mayor que la fecha de fin.",
        )

    if start_date is not None:
        query = query.filter(Venta.dia >= start_date)

    if end_date is not None:
        query = query.filter(Venta.dia <= end_date)

    if limit is not None:
        if limit <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El límite debe ser un número positivo.",
            )
    else:
        limit = 5
    query = query.limit(limit)

    if page is not None:
        if page <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La página debe ser un número positivo.",
            )
    else:
        page = 1
    query = query.offset((page - 1) * limit)

    return [mostrarventasimple(venta) for venta in query.all()]


@router.get("/{id}", response_model=VentaDetalleRespuesta)
def obtener_venta(id: int, db: Session = Depends(get_db)):
    venta = busquedaventa(id, db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    carrito = busquedacarrito(venta.carrito_id, db)
    if carrito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")
        
    return mostrarventa(venta, db)


@router.put("/{id}", response_model=VentaDetalleRespuesta)
def modificar_venta(id: int, datos: VentaCrear, db: Session = Depends(get_db)):
    venta = busquedaventa(id, db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    carrito_actual = busquedacarrito(venta.carrito_id, db)
    if getestadocarrito(carrito_actual) != "abierto":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede modificar una venta si el carrito está cerrado."
        )

    carrito_nuevo = busquedacarrito(datos.carrito_id, db)
    if carrito_nuevo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El carrito nuevo no existe.")

    if carrito_nuevo.venta is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este carrito ya esta asociado a una venta."
        )
    
    modificarventa(venta,datos,db)
    return mostrarventa(venta,db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(id: int, db: Session = Depends(get_db)):
    venta = busquedaventa(id, db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    carrito = busquedacarrito(venta.carrito_id, db)
    if carrito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")
    
    if getestadocarrito(carrito, db) != "cerrado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,detail="No se puede eliminar una venta cuyo carrito está cerrado.")
            
    borrarventa(venta, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{id}/carrito", status_code=status.HTTP_201_CREATED) 
def enlazar_venta(
    id: int,
    carrito: int,
    db: Session = Depends(get_db),
):
    venta = busquedaventa(id, db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")
  
    if getcarritoventa(venta):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La venta ya tiene un carrito asociado.") 
    
    if carrito == -1: 
        modificarventa(venta,VentaCrear(dia_venta=getdiaventa(venta),hora_venta=gethoraventa(venta),carrito_id=0),db)
        return {"detail": "Carrito desvinculado de la venta."}
     

    carritos = busquedacarrito(carrito, db)
    if carritos is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    if getestadocarrito(carritos) != "cerrado":
        raise HTTPException(status_code=409, detail="No se puede asociar un carrito abierto a una venta.")
    
    datos = VentaCrear(
        dia_venta=getdiaventa(venta),
        hora_venta=gethoraventa(venta),
        carrito_id=getidcarrito(carritos)
    )

    modificarventa(venta,datos,db)
    
    return {"detail" : "Venta finalizada" }



