from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy.orm import Session

from database import get_db
from models import  Venta
from ventas import altaventa, ventasgen, busquedaventa, modificarventa, borrarventa,mostrarventa
from carrito import busquedacarrito,modifcarrito
from schema import VentaCrear,VentaListaRespuesta,VentaDetalleRespuesta

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_venta(datos: VentaCrear, db: Session = Depends(get_db)):
    carrito = busquedacarrito(datos.carrito_id,db)
    if carrito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")

    venta_existente = db.query(Venta).filter(Venta.carrito_id == datos.carrito_id).first()
    if venta_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este carrito ya esta asociado a una venta")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")
        
    return mostrarventa(venta, db)


@router.put("/{id}", response_model=VentaDetalleRespuesta)
def modificar_venta(id: int, datos: VentaCrear, db: Session = Depends(get_db)):
    venta = busquedaventa(id,db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    carrito_actual = busquedacarrito(venta.carrito_id, db)
    if carrito_actual is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El carrito de la venta no existe.")

    if carrito_actual.estado != "abierto":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede modificar una venta si el carrito está cerrado."
        )
    carrito_nuevo = busquedacarrito(datos.carrito_id, db)
    if carrito_nuevo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El carrito nuevo no existe.")

    if carrito_nuevo.estado != "abierto":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede asignar una venta a un carrito cerrado."
        )
    modificarventa(venta,datos,db)
    return mostrarventa(venta,db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(id: int, db: Session = Depends(get_db)):
    venta = busquedaventa(id,db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")
    
    carrito = busquedacarrito(venta.carrito_id, db)
    if carrito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")

    if carrito.estado == "cerrado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,detail="No se puede eliminar una venta cuyo carrito está cerrado.")
    borrarventa(venta, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{id}/carrito",status_code=status.HTTP_201_CREATED)
def enlazar_venta(
    id : int,
    carrito : int,
    db : Session=Depends(get_db)
):
    venta = busquedaventa(id,db)
    if venta is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")
    
    carritos = busquedacarrito(carrito,db)
    if carritos is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    datos = VentaCrear(
        dia_venta=venta.dia,
        hora_venta=venta.hora,
        carrito_id=carritos.id
    )
    carritomod = busquedacarrito(carrito,db)
    carritomod.estado = "cerrado" 
    modificarventa(venta,datos,db)
    modifcarrito(carritos,carritomod,db)
    return {"detail" : "Venta finalizada" }




