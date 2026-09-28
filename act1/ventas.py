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

def gettotal_venta(venta):
    return venta.total_venta

def setdiaventa(venta,dia):
    venta.dia=dia
    return venta

def sethoraventa(venta,hora):
    venta.hora=hora
    return venta

def setcarritoventa(venta,carrito):
    venta.carrito_id=carrito
    return venta

def settotal_venta(venta,total):
    venta.precio_total = total
 
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
        settotal_venta(venta,totalventa(venta,db))
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
            "carrito_id": v.carrito_id,
            "precio_total": v.total
        }
        for v in ventas
    ]         

def busquedaventa(id,db):
    return db.query(Venta).filter(Venta.id == id).first()

def subtotalventa(precio,cantidad):
    return precio * cantidad

def totalventa(venta,db):
    carrito = busquedacarrito(getcarritoventa(venta),db)
    precio_total = 0.0
    
    if carrito:
        items = busquedaprod_carrito_productosencarrito(carrito.id,db)
    
        for item in items:
            producto = item.producto
            if producto is None:
                continue

            subtotal = subtotalventa(producto.precio,item.cantidad)
            precio_total += subtotal
   
    return precio_total
    

def mostrarventasimple(venta,db):
    carrito = busquedacarrito(getcarritoventa(venta),db)
    productos = []
    
    if carrito:
        items = busquedaprod_carrito_productosencarrito(carrito.id,db)

        for item in items:
            producto = item.producto
            if producto is None:
                continue

            productos.append({
                "id": item.id,
                "nombre": producto.nombre
            })

    return {
        "id": getidventa(venta),
        "fecha": getdiaventa(venta),
        "hora": gethoraventa(venta),
        "precio_total": gettotal_venta(venta),
        "carrito": {
            "id": carrito.id if carrito else None,
            "fecha_creacion": carrito.fecha_creacion if carrito else None,
            "estado": carrito.estado if carrito else None
        } if carrito else None
    }

def mostrarventa(venta, db):
    carrito = busquedacarrito(getcarritoventa(venta),db)
    productos = []

    if carrito:
        items = busquedaprod_carrito_productosencarrito(carrito.id,db)

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
        "id": getidventa(venta),
        "fecha": getdiaventa(venta),
        "hora": gethoraventa(venta),
        "precio_total": gettotal_venta(venta),
        "carrito": {
            "id": carrito.id if carrito else None,
            "fecha_creacion": carrito.fecha_creacion if carrito else None,
            "estado": carrito.estado if carrito else None,
            "productos": productos
        } if carrito else None
    }
