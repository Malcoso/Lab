from pydantic import BaseModel,ConfigDict
from datetime import date,time

class ProductoCrear(BaseModel):                         #Input producto
    nombre: str
    precio: float

class ProductoRespuesta(BaseModel):                     #Lo que se va mostrar del producto 
    id: int
    nombre : str
    precio : float
    model_config = ConfigDict(from_attributes=True)

class VentaCrear(BaseModel):                            #Input venta
    dia_venta : date
    hora_venta : time
    producto_id: int
    cantidad: int

class VentaRespuesta(BaseModel):                        #Lo que se va mostrar de la venta
    id: int
    dia: date
    hora: time
    carrito : CarritoRespuesta

    model_config = ConfigDict(from_attributes=True)

class CarritoCrear(BaseModel):
    dia : date
    estado : str

class CarritoRespuesta(BaseModel):
    carrito_id : int
    dia_creacion : date
    estado : str
    productos : ProductoRespuesta
    
    model_config = ConfigDict(from_attributes=True)

class Carrito_ProductoCrear(BaseModel):
    id_carrito: int
    id_producto : int
    cantidad : int

class Carrito_ProductoRespuesta(BaseModel):
    id_carrito : int
    id_producto : int
    cantidad : int
