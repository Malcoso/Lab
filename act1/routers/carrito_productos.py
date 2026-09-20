from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from carrito_producto import altacarrito_producto,mostrarcarrito_producto
from carrito_producto import busq_prod_carrito,borrar_prod_carrito,busquedacarritos_prod
from carrito import busquedacarrito
from productos import busquedaprod
from schema import Carrito_ProductoCrear, Carrito_ProductoRespuesta,Carrito_ProductoRespuestas
from models import Carrito_Producto
router = APIRouter(prefix="/carritos", tags=["carrito_productos"])


@router.post("/{id}/productos", response_model=Carrito_ProductoRespuestas, status_code=status.HTTP_201_CREATED)
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
            if busquedaprod(datos.id_producto,db):
                if datos.cantidad > 0:
                        item = altacarrito_producto(id,datos, db)
                        return mostrarcarrito_producto(item)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cantidad debe ser mayor a 0")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el producto")

        if carrito_existente.estado == 'cerrado':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El carrito ya fue usado")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el carrito")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create carrito_producto: {e}")

@router.get("/{id}/productos",response_model=list[Carrito_ProductoRespuesta])
def listar_carrito_producto(
        id : int,
        db : Session = Depends(get_db),
    ):
        carrito = busquedacarrito(id,db)
        if carrito is None:
            raise HTTPException(status_code=404, detail="No existe el carrito")
        items = busquedacarritos_prod(id,db)
        if items == []:
             raise HTTPException(status_code=404, detail="No hay productos en el carrito")
        return [mostrarcarrito_producto(item) for item in items]

@router.get("/{idcarrito}/productos/{id}",response_model=list[Carrito_ProductoRespuesta])
def listar_carrito_producto(
        idcarrito : int,
        id : int,
        db : Session = Depends(get_db),
    ):
        carrito = busquedacarrito(idcarrito,db)
        if carrito is None:
            raise HTTPException(status_code=404, detail="No existe el carrito")
        item = busq_prod_carrito(db,idcarrito,id)
        if item is None:
             raise HTTPException(status_code=404, detail="No hay productos en el carrito")
        return [mostrarcarrito_producto(item)]

@router.delete("/{idcarrito}/productos/{id}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto_carrito(
     idcarrito: int,
     id : int, 
     db: Session = Depends(get_db)
):
    carrito = busquedacarrito(idcarrito,db)
    if carrito is None:
        raise HTTPException(status_code=404, detail="No existe el carrito")
    item = busq_prod_carrito(db,idcarrito,id)
    if item is None:
        raise HTTPException(status_code=404, detail="No existe el carrito_producto")
    borrar_prod_carrito(db,item)
    return {"detail" : "carrito_producto eliminado"}