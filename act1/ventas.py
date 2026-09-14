from models import Producto, Venta
from productos import mostrarprod
from database import session
from datetime import date, datetime,time
 
def altaventa(venta, db):
    try:
        producto = db.get(Producto,venta.producto_id)
        if producto is None:
            print("Producto no encontrado. No se puede realizar la venta.")
            return

        venta.precio_total = producto.precio * venta.cantidad
        
        db.add(venta)
        db.commit()
        db.refresh(venta)
        return venta
    except Exception as e:
        db.rollback()
        raise e

def mostrarventa(venta):
    return {
        "id Venta": venta.id,
        "dia": venta.dia,
        "hora": venta.hora,
        "producto_id": venta.producto_id,
        "producto": mostrarprod(venta.producto),
        "cantidad": venta.cantidad,
        "precio_total": venta.precio_total
    }

def borrarventa(venta,db):
    try:
        db.delete(venta)
        db.commit()
        return venta
    except Exception as e:
        raise e

def modificarventa(venta,datos,db):
    try:
        venta.producto_id= datos.producto_id
        venta.cantidad= datos.cantidad
        venta.precio_total=datos.producto.precio * datos.cantidad
        db.commit()
        db.refresh(venta)
    except Exception as e:
        raise e



def ventasgen(db):
    ventas = db.query(Venta).all()
    return ventas

def busquedaventa(id,db):
    venta = db.query(Venta).filter_by(id=id).first()
    if venta:
        return venta
    else:
        return None

