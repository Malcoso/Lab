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

class AsociarVenta(BaseModel):
    carrito_id: int

class VentaListaRespuesta(BaseModel):
    id: int
    dia: date
    hora: time
    carrito_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

class VentaDetalleRespuesta(BaseModel):
    id: int
    fecha: date
    hora: time
    precio_total: float
    carrito: CarritoRespuestaDetalle | None = None

    model_config = ConfigDict(from_attributes=True)
    
class CarritoCrear(BaseModel):
    fecha_creacion : date
    estado : str

class ProductoEnCarrito(BaseModel):
    id : int
    nombre : str
    precio_unitario: float
    cantidad: int
    subtotal: float

class CarritosRespuesta(BaseModel):
    id : int
    fecha_creacion : date
    estado : str

    model_config = ConfigDict(from_attributes=True)
    
class CarritoRespuestaDetalle(BaseModel):
    id : int
    fecha_creacion : date
    estado : str

    productos : list[ProductoEnCarrito]
    total : float
    model_config = ConfigDict(from_attributes=True)

class CarritoRespuesta(BaseModel):
    id : int
    fecha_creacion : date
    estado : str

    productos : list[ProductoEnCarrito]
    model_config = ConfigDict(from_attributes=True)


class Carrito_ProductoCrear(BaseModel):
    id_producto : int
    cantidad : int

class Carrito_ProductoRespuesta(BaseModel):
    id : int
    id_producto : int
    cantidad : int
    subtotal : float
    producto : ProductoRespuesta | None = None

    model_config=ConfigDict(from_attributes=True)

class Carrito_ProductoRespuestaDetalle(BaseModel):
    id : int
    id_producto : int
    cantidad : int    
    producto : ProductoRespuesta | None = None

    model_config=ConfigDict(from_attributes=True)