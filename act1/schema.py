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
    producto_id: int
    producto : ProductoRespuesta
    cantidad: int
    precio_total: float

    model_config = ConfigDict(from_attributes=True)