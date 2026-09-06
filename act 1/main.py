from datetime import date, datetime,time
from fastapi import FastAPI,Depends,HTTPException,status

from pydantic import BaseModel,ConfigDict
from sqlalchemy.orm import Session
from typing import Generator

from models import Producto, Venta
from productos import altaprod, productosgen,busquedaprod,modifprod,borraprod
from ventas import altaventa,ventasgen,busquedaventa,modificarventa,borrarventa
from database import sessionLocal

app = FastAPI()

class ProductoCrear(BaseModel):                         #Input producto
    nombre: str
    precio: float

class ProductoRespuesta(BaseModel):                     #Lo que se va mostrar del producto 
    id: int
    nombre : str
    precio : float
    model_config = ConfigDict(from_attributes=True)

class VentaCrear(BaseModel):                            #Input venta
    producto_id: int
    cantidad: int

class VentaRespuesta(BaseModel):                        #Lo que se va mostrar de la venta
    id: int
    dia: date
    hora: time
    producto_id: int
    producto : ProductoRespuesta
    cantidad: int
    precio_total: float

    model_config = ConfigDict(from_attributes=True)

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
    producto = Producto(nombre=datos.nombre,precio=datos.precio)                                #Se almacena el producto
    altaprod(producto, db)
    return {"detail": "Producto dado de alta"}                                                               

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
    return {"detail": "Producto modificado" }


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
    
    venta = Venta(dia=date.today(),
        hora=datetime.now().time(),
        producto_id=datos.producto_id,        
        cantidad=datos.cantidad,
        precio_total=producto.precio * datos.cantidad
    )
    altaventa(venta, db)
    return {"detail": "Venta dada de alta"}


@app.get("/ventas/",response_model=list[VentaRespuesta])
def listar_ventas(
    db: Session = Depends(obtener_session)
):
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

    return {"detail": "Venta modificada"}


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
