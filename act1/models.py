from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Time
from sqlalchemy.orm import declarative_base, relationship


base = declarative_base()

class Producto(base):
    __tablename__ = 'productos'
    id = Column(Integer, autoincrement=True, primary_key=True)
    nombre = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)
    ventas = relationship('Venta', back_populates='producto')

class Venta(base):
    __tablename__ = 'ventas'
    id = Column(Integer, autoincrement=True, primary_key=True)
    dia = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'))
    producto = relationship('Producto', back_populates='ventas')
    cantidad = Column(Integer, nullable=False)
    precio_total = Column(Float, nullable=False) #ELIMINAR
