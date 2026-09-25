from models import Venta
from carrito_producto import busquedaprod_carrito_productosencarrito
from carrito import busquedacarrito
def getidventa(venta):
    return venta.id

def getdiaventa(venta):
    return venta.dia

def gethoraventa(venta):
    return venta.hora

def getcarritoventa(venta):
    return venta.carrito_id

def setdiaventa(venta,dia):
    venta.dia=dia
    return venta

def sethoraventa(venta,hora):
    venta.hora=hora
    return venta

def setcarritoventa(venta,carrito):
    venta.carrito_id=carrito
    return venta
 
def altaventa(venta, db):
    try:
        db.add(venta)
        db.commit()
        db.refresh(venta)
        return venta
    
    except Exception as e:
        db.rollback()
        raise e

def borrarventa(venta,db):
    try:
        db.delete(venta)
        db.commit()
        return venta
    except Exception as e:
        db.rollback()
        raise e

def modificarventa(venta,datos,db):
    try:
        setdiaventa(venta,datos.dia)
        sethoraventa(venta,datos.hora)
        setcarritoventa(venta,datos.carrito_id)
        db.commit()
        db.refresh(venta)
    except Exception as e:
        db.rollback()
        raise e


def ventasgen(db):
    ventas = db.query(Venta).all()
    return [
        {
            "id": v.id,
            "dia": v.dia,
            "hora": v.hora,
            "carrito_id": v.carrito_id
        }
        for v in ventas
    ]         

def busquedaventa(id,db):
    return db.query(Venta).filter(Venta.id == id).first()


def mostrarventa(venta, db):
    carrito = busquedacarrito(getcarritoventa(venta),db)
    productos = []
    precio_total = 0.0

    if carrito:
        items = busquedaprod_carrito_productosencarrito(carrito.id,db)

        for item in items:
            producto = item.producto
            if producto is None:
                continue

            subtotal = producto.precio * item.cantidad
            precio_total += subtotal

            productos.append({
                "id": item.id,
                "nombre": producto.nombre,
                "precio_unitario": producto.precio,
                "cantidad": item.cantidad,
                "subtotal": subtotal
            })

    return {
        "id": getidventa(venta),
        "fecha": getdiaventa(venta),
        "hora": gethoraventa(venta),
        "precio_total": precio_total,
        "carrito": {
            "id": carrito.id if carrito else None,
            "fecha_creacion": carrito.fecha_creacion if carrito else None,
            "estado": carrito.estado if carrito else None,
            "productos": productos,
            "total": precio_total
        } if carrito else None
    }
