from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Producto
from productos import altaprod, productosgen, busquedaprod, modifprod, borraprod
from schema import ProductoCrear, ProductoRespuesta

router = APIRouter(prefix="/productos", tags=["productos"])


@router.post("", response_model=ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_producto(
    datos: ProductoCrear,
    db: Session = Depends(get_db),
):
    try:
        nombre = datos.nombre.strip()
        producto_existente = db.query(Producto).filter(Producto.nombre == nombre).first()

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
def listar_productos(db: Session = Depends(get_db)):
    return productosgen(db)


@router.get("/{id}", response_model=ProductoRespuesta)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = db.get(Producto, id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    return busquedaprod(id, db)


@router.put("/{id}", response_model=ProductoRespuesta)
def modificar_producto(id: int, datos: ProductoCrear, db: Session = Depends(get_db)):
    producto = db.get(Producto, id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    nombre = datos.nombre.strip()
    producto_existente = db.query(Producto).filter(Producto.nombre == nombre).first()
    if producto_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El producto ya existe.",
            )
    if datos.precio <=0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "El producto tiene que tener un valor mayor a 0")
    
    return modifprod(producto, datos, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    producto = db.get(Producto, id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")

    borraprod(producto, db)
    return {"detail": "Producto eliminado."}
