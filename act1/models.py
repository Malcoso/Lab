from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Time
from sqlalchemy.orm import declarative_base, relationship


base = declarative_base()

class Producto(base):
    __tablename__ = 'productos'
    id = Column(Integer, autoincrement=True, primary_key=True)
    nombre = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)

    carrito_productos = relationship('Carrito_Producto',back_populates='producto')

class Venta(base):
    __tablename__ = 'ventas'
    id = Column(Integer, autoincrement=True, primary_key=True)
    dia = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)

    carrito_id = Column(Integer,ForeignKey('carritos.id'))
    carrito = relationship('Carrito',back_populates='venta')

class Carrito(base):
    __tablename__ = 'carritos'
    id = Column(Integer,autoincrement=True,primary_key=True)
    fecha_creacion=Column(Date,nullable=False)
    estado=Column(String(20),default='abierto',nullable=False)

    venta = relationship('Venta',back_populates='carrito')
    carrito_productos = relationship('Carrito_Producto', back_populates='carrito')


class Carrito_Producto(base):
    __tablename__ = 'carrito_productos'
    id = Column(Integer,autoincrement=True,primary_key=True)

    id_carrito=Column(Integer, ForeignKey('carritos.id'))
    carrito= relationship('Carrito',back_populates='carrito_productos')

    id_producto=Column(Integer, ForeignKey('productos.id'))
    producto = relationship('Producto', back_populates='carrito_productos')
    
    cantidad=Column(Integer,nullable=False)

