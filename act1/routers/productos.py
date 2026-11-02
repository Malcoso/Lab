from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Producto

from productos import altaprod, modifprod, borraprod
from productos import productosgen,busquedaprod,busquedaprodnombre
from carrito_producto import buquedaprod_carrito_producto

from schema import ProductoCrear, ProductoRespuesta

router = APIRouter(prefix="/productos", tags=["productos"])


@router.post("", response_model=ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_producto(
    datos: ProductoCrear,
    db: Session = Depends(get_db),
):
    try:
        nombre = datos.nombre.strip()
        producto_existente = busquedaprodnombre(nombre,db)

        if producto_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El producto ya existe.",
            )
        if datos.precio <=0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "El producto tiene que tener un valor mayor a 0")
        
        producto = Producto(nombre=nombre, precio=datos.precio)
        return altaprod(producto, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to create product: {e}",
        )


@router.get("/", response_model=list[ProductoRespuesta])
def listar_productos(
     db: Session = Depends(get_db),
     start_date: Optional[date] = None,             
     end_date : Optional[date] = None,
     limit: Optional[int] = None,
     page : Optional[int] = None                
    ):

    query = db.query(Producto)

    if start_date and end_date is not None:
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio no puede ser mayor que la fecha de fin.",
            )

    if start_date is not None:
        query = query.filter(Producto.fecha_creacion >= start_date)     

    if  end_date is not None:
        query = query.filter(Producto.fecha_creacion <= end_date)

    if limit is not None:
        if limit <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El límite debe ser un número positivo.",
            )
        query = query.limit(limit)
    else:
        limit = 5
        query = query.limit(limit)

    if page is not None:
        if page <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La página debe ser un número positivo.",
            )
        offset = (page - 1) * limit
        query = query.offset(offset)
    else:
        page = 1
        offset = (page - 1) * limit
        query = query.offset(offset)

         
    return productosgen(query)


@router.get("/{id}", response_model=ProductoRespuesta)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = busquedaprod(id,db)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    return busquedaprod(id, db)


@router.put("/{id}", response_model=ProductoRespuesta)
def modificar_producto(id: int, datos: ProductoCrear, db: Session = Depends(get_db)):
    producto = busquedaprod(id,db)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    nombre = datos.nombre.strip()
    producto_existente = busquedaprodnombre(nombre,db)
    if producto_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El producto ya existe.",
            )

    if datos.precio <=0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "El producto tiene que tener un valor mayor a 0")

    producto_usado = buquedaprod_carrito_producto(id,db)
    if producto_usado: 
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "El producto fue utilizado en un carrito")  
    
    return modifprod(producto, datos, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    producto = busquedaprod(id,db)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    
    producto_usado = buquedaprod_carrito_producto(id,db)
    if producto_usado: 
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "El producto fue utilizado en un carrito")
    borraprod(producto, db)
    return {"detail": "Producto eliminado."}
