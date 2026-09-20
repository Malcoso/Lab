from models import Carrito,Carrito_Producto
from productos import busquedaprod
from carrito_producto import busquedacarrito_prod
def altacarrito(carrito,db):
    try:
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
        print("Carrito agregado.")
        return carrito
    except Exception as e:
        db.rollback()
        raise e

def mostrarcarrito(carrito,db):
    items = db.query(Carrito_Producto).filter_by(id_carrito=carrito.id).all()

    productos = []


    for item in items:
        producto = item.producto
        if producto is None:
            continue

        subtotal = producto.precio * item.cantidad

        productos.append({
            "id": item.id,
            "nombre": producto.nombre,
            "precio_unitario": producto.precio,
            "cantidad": item.cantidad,
            "subtotal": subtotal
        })

    return {
        "id": carrito.id,
        "fecha_creacion": carrito.fecha_creacion,
        "estado": carrito.estado,
        "productos": productos,

    }

def modifcarrito(carrito,datos,db):
    try:
        carrito.fecha_creacion=datos.fecha_creacion
        carrito.estado=datos.estado
        db.commit()
        db.refresh(carrito)
        print("carrito modificado")
        return carrito
    except Exception as e:
        db.rollback()
        raise e

def carritosgen(db):                       
    carritos = db.query(Carrito).all()
    if carritos:
        return carritos
    else:
        return None

def busquedacarrito(id,db):   
    carritos = db.query(Carrito).filter_by(id=id).first()
    if carritos:
        return carritos
    else:
        return None

def borrarcarrito(carrito,db):
    try:
        db.delete(carrito)
        db.commit()
        print("Carrito eliminado")
        return carrito
    except Exception as e:
        db.rollback()
        raise e

#deberia mover los carrito_producto a su propio coso

