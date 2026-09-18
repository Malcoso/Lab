from fastapi import FastAPI,Depends,HTTPException,status

from sqlalchemy.orm import Session
from typing import Generator

from models import Producto, Venta,Carrito,Carrito_Producto
from productos import altaprod, productosgen,busquedaprod,modifprod,borraprod
from ventas import altaventa,ventasgen,busquedaventa,modificarventa,borrarventa
from database import sessionLocal
from schema import ProductoCrear, ProductoRespuesta, VentaCrear,VentaRespuesta
app = FastAPI()

def obtener_session()-> Generator[Session,None,None]:   #Se obtiene la sesion de la base de datos
    db = sessionLocal()
    try:
        yield db                                        #Devuelve la sesion para usarse y sigue
    finally:
        db.close()                                      #Cierra sesion

@app.post("/productos",response_model=ProductoRespuesta,status_code=status.HTTP_201_CREATED)    #Para crear el producto
def crear_producto(
    datos:ProductoCrear,
    db: Session = Depends(obtener_session)
):
    try:
        nombre = datos.nombre.strip()
        producto_existente = db.query(Producto).filter(Producto.nombre == nombre).first()

        if producto_existente:
            raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
                detail="El producto ya existe."
            )

        producto = Producto(nombre=nombre, precio=datos.precio)

        return altaprod(producto, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create product: {e}")    
                                                          

@app.get("/productos/",response_model=list[ProductoRespuesta],)                                 #Recibir todos los productos
def listar_productos(
    db: Session = Depends(obtener_session)
):
    return productosgen(db)                                                                     #Retorna todos los productos 


@app.get("/productos/{id}",response_model=ProductoRespuesta)                                    #Recibir producto por id
def obtener_producto(
    id:int,
    db: Session = Depends(obtener_session)
):
    producto = db.get(Producto,id)                                                              #Busca si existe el producto
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    return busquedaprod(id, db)                                                                 #Retorna el producto


@app.put("/productos/{id}",response_model=ProductoRespuesta)                                    #Modificar producto
def modificar_producto(
    id:int,
    datos:ProductoCrear,
    db: Session = Depends(obtener_session)
):
    producto = db.get(Producto,id)                                                              #Busca el producto
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    
    modifprod(producto,datos,db)                                                                #Modifica el producto
    return producto


@app.delete("/productos/{id}",status_code=status.HTTP_204_NO_CONTENT)                           #Eliminar productos
def eliminar_producto(
    id:int,
    db: Session = Depends(obtener_session)
):
    producto = db.get(Producto,id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    
    borraprod(producto,db)                                                                      #Elimina el producto
    return {"detail": "Producto eliminado."}                                                    #Da confirmacion


@app.post("/ventas",response_model=VentaRespuesta,status_code=status.HTTP_201_CREATED)        #Alta ventas
def crear_venta(
    datos: VentaCrear,
    db: Session = Depends(obtener_session)
):
    producto = db.get(Producto, datos.producto_id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado. No se puede realizar la venta.")

    if datos.cantidad <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cantidad debe ser mayor que cero.")
    
    venta = Venta(dia=datos.dia_venta,
        hora=datos.hora_venta,
        producto_id=datos.producto_id,        
        cantidad=datos.cantidad,
        precio_total=producto.precio * datos.cantidad
    )
    altaventa(venta, db)
    return venta


@app.get("/ventas/",response_model=list[VentaRespuesta])
def listar_ventas(
    db: Session = Depends(obtener_session)
):
    #EL PRECIOTOTAL TIENE QUE ESTAR CALCULADO ACA
    return ventasgen(db)


@app.get("/ventas/{id}",response_model=VentaRespuesta)
def obtener_venta(
    id:int,
    db: Session = Depends(obtener_session)
):
    venta = busquedaventa(id, db)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")
    return venta


@app.put("/ventas/{id}",response_model=VentaRespuesta)
def modificar_venta(
    id:int,
    datos:VentaCrear,
    db: Session = Depends(obtener_session)
):
    venta = db.get(Venta,id)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")
    
    producto = db.get(Producto, datos.producto_id)
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado. No se puede modificar la venta.")

    if datos.cantidad <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cantidad debe ser mayor que cero.")

    modificarventa(venta,producto,datos,db)

    return venta


@app.delete("/ventas/{id}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(
    id:int,
    db: Session = Depends(obtener_session)
):
    venta = db.get(Venta,id)
    if venta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")
    
    borrarventa(venta,db)
    return {"detail": "Venta eliminada."}
