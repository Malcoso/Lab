from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Carrito
from carrito import altacarrito, carritosgen, busquedacarrito, modifcarrito, borrarcarrito
from schema import CarritoCrear, CarritoRespuesta

router = APIRouter(prefix="/carritos", tags=["carritos"])


@router.post("", response_model=CarritoCrear, status_code=status.HTTP_201_CREATED)
def crear_carrito(carrito: CarritoCrear, db: Session = Depends(get_db)):
    if carrito.estado == 'abierto':
        try:
            carritos = Carrito(fecha_creacion=carrito.dia, estado=carrito.estado)
            return altacarrito(carritos, db)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create carrito: {e}")
    elif carrito.estado == 'cerrado':
        raise HTTPException(status_code=400, detail="No se ha hecho el carrito")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el estado escrito")


@router.get("/", response_model=list[CarritoRespuesta])
def listar_carritos(db: Session = Depends(get_db)):
    return carritosgen(db)


@router.get("/{id}", response_model=CarritoRespuesta)
def obtener_carrito(id: int, db: Session = Depends(get_db)):
    return busquedacarrito(id, db)


@router.put("/{id}", response_model=CarritoRespuesta)
def modificar_carrito(id: int, datos: CarritoCrear, db: Session = Depends(get_db)):
    carrito = db.get(Carrito, id)
    if carrito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")

    if carrito.venta:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se puede alterar un carrito ya utilizado")

    if datos.estado == 'cerrado' or datos.estado == 'abierto':
        return modifcarrito(carrito, datos, db)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el estado escrito")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_carrito(id: int, db: Session = Depends(get_db)):
    carrito = db.get(Carrito, id)
    if carrito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado.")

    if carrito.venta:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se puede eliminar un carrito ya utilizado")

    borrarcarrito(carrito, db)
    return {"detail": "Carrito eliminado."}
