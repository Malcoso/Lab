from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from carrito_producto import altacarrito_producto
from carrito import busquedacarrito
from productos import busquedaprod
from schema import Carrito_ProductoCrear, Carrito_ProductoRespuesta

router = APIRouter(prefix="/carritos", tags=["carrito_productos"])


@router.post("/{id}/productos", response_model=Carrito_ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_carrito_producto(
    id: int,
    datos: Carrito_ProductoCrear,
    db: Session = Depends(get_db),
):
    try:

        carrito_existente = busquedacarrito(id, db)
        if carrito_existente is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el carrito")

        if carrito_existente.estado == 'abierto':
            if busquedaprod(datos.id_producto):
                if datos.cantidad > 0:
                    return altacarrito_producto(datos, db)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cantidad debe ser mayor a 0")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el producto")

        if carrito_existente.estado == 'cerrado':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El carrito ya fue usado")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el carrito")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create carrito_producto: {e}")
