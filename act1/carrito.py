from models import Carrito
from carrito_producto import busquedaprod_carrito_productosencarrito

def getidcarrito(carrito):
    return carrito.id

def getfecha_creacioncarrito(carrito):
    return carrito.fecha_creacion

def getestadocarrito(carrito):
    return carrito.estado

def setfecha_creacioncarrito(carrito,nuevafecha):
    carrito.fecha_creacion=nuevafecha
    return carrito

def setestadocarrito(carrito,estado):
    carrito.estado = estado
    return carrito

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
    items = busquedaprod_carrito_productosencarrito(carrito.id,db)

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
        "id": getidcarrito(carrito),
        "fecha_creacion": getfecha_creacioncarrito(carrito),
        "estado": getestadocarrito(carrito),
        "productos": productos,

    }

def modifcarrito(carrito,datos,db):
    try:
        setfecha_creacioncarrito(carrito,datos.fecha_creacion)
        setestadocarrito(carrito,datos.estado)
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
        
        return [mostrarcarrito(c,db) for c in carritos]
    else:
        return None

def busquedacarrito(id,db):   
    return db.query(Carrito).filter(Carrito.id ==id).first()
    
def borrarcarrito(carrito,db):
    try:
        db.delete(carrito)
        db.commit()
        print("Carrito eliminado")
        return carrito
    except Exception as e:
        db.rollback()
        raise e

