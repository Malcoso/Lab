from models import Carrito,Carrito_Producto
from productos import busquedaprod
from carrito_producto import busquedacarrito_prod
def altacarrito(carrito,db):
    try:
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
        print("Producto agregado.")
        return carrito
    except Exception as e:
        db.rollback()
        raise e

def mostrarcarrito(carrito,db):
    items = busquedacarrito_prod(carrito.id,db)

    productos = []
    total = 0

    for item in items:
        producto = busquedaprod(item.id,db)
        if producto:
            subtotal = producto.precio * item.cantidad
            total +=subtotal
            productos.append({
                "id_producto": producto.id,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "cantidad": item.cantidad,
                "subtotal": subtotal
            })
    return {
        "ID Carrito ": carrito.id,
        "Fecha de creacion ": carrito.fecha_creacion,
        "Estado ": carrito.estado,
        "Productos ": productos,
        "Total " : total
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

