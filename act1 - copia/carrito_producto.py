from models import Carrito_Producto
from productos import mostrarprod
def altacarrito_producto(carrito_producto,db):
    try:
        db.add(carrito_producto)
        db.commit()
        db.refresh(carrito_producto)
        print("Item agregado al carrito")
        return carrito_producto
    except Exception as e:
        db.rollback()
        raise e

def mostrarcarrito_producto(carrito_producto):
    return {
        "ID Carrito_Producto ": carrito_producto.id,
        "ID Producto ": carrito_producto.id_producto,
        "Producto ": mostrarprod(carrito_producto.producto),
        "Cantidad producto": carrito_producto.cantidad
    }


def carrito_prodgen(db):
    carrito_prod=db.query(Carrito_Producto).all()
    if carrito_prod:
        return carrito_prod
    else:
        return None

def busquedacarrito_prod(id,db):
    carrito_prod=db.query(Carrito_Producto).filterby(id=id).first()
    if carrito_prod:
        return carrito_prod
    else:
        return None

def busquedacarritos_prod(id_carrito,db):
    carrito_producto=db.query(carrito_producto).filterby(id_carrito=id_carrito).all()
    return carrito_producto

#Hacer en el main.py
def alta_carrito(db,id_carrito,id_producto,cantidad):
    item = db.query(Carrito_Producto).filter_by(
        id_carrito=id_carrito,
        id_producto=id_producto
    ).first()
    if item:
        item.cantidad+=cantidad
    else:
        item = Carrito_Producto(
            id_carrito=id_carrito,
            id_producto=id_producto,
            cantidad=cantidad
        )
        db.add(item)
    db.commit()
    return item

def busq_prod_carrito(db,id_carrito,id_producto):
    carrito_producto = db.query(carrito_producto).filterby(id_carrito=id_carrito,id_producto=id_producto).first()
    if carrito_producto:
        return carrito_producto
    else:
        return None