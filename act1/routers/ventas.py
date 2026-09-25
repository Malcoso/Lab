from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy.orm import Session

from database import get_db
from models import  Venta
from ventas import altaventa, ventasgen, busquedaventa, modificarventa, borrarventa,mostrarventa
from ventas import getdiaventa,gethoraventa,getcarritoventa
from carrito import busquedacarrito
from schema import VentaCrear,VentaListaRespuesta,VentaDetalleRespuesta

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_venta(datos: VentaCrear, db: Session = Depends(get_db)):

    venta = Venta(
        dia=datos.dia_venta,
        hora=datos.hora_venta,
        carrito_id = None
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

    return mostrarventa(venta, db)


@router.put("/{id}", response_model=VentaDetalleRespuesta)
def modificar_venta(id: int, datos: VentaCrear, db: Session = Depends(get_db)):
    venta = busquedaventa(id,db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    carrito_actual = busquedacarrito(getcarritoventa(venta), db)
    if carrito_actual is not None:
        if carrito_actual.estado == 'Cerrado':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se puede modificar una venta cerrada")
        else:
            venta = Venta(
            dia=datos.dia_venta,
            hora=datos.hora_venta,
            carrito_id = carrito_actual.id
        )
    else:
        venta = Venta(
        dia=datos.dia_venta,
        hora=datos.hora_venta,
        carrito_id = None
        )
        
    modificarventa(venta,datos,db)
    return mostrarventa(venta,db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(id: int, db: Session = Depends(get_db)):
    venta = busquedaventa(id,db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")
    
    carrito = busquedacarrito(getcarritoventa(venta), db)
    if carrito is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se puede borrar una venta con un carrito ya asignado.")

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
    
    if carrito==-1:
        datos = Venta(
                dia=getdiaventa(venta),
                hora=gethoraventa(venta),
                carrito_id = None
            )
        modificarventa(venta,datos,db)
        return {"detail": "Venta desvinculada"}
    
    carritos = busquedacarrito(carrito,db)
    if carritos is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    if carritos.venta:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="El carrito ya tiene asignado una venta")
        
    if carritos.estado!= 'cerrado':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail ="El carrito tiene que estar cerrado para continuar")
    
    datos = Venta(
            dia=getdiaventa(venta),
            hora=gethoraventa(venta),
            carrito_id = carrito
    )
    modificarventa(venta,datos,db)
    return {"detail" : "Venta finalizada" }




