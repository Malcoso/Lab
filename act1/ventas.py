from models import Venta,Carrito_Producto

 
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
        venta.dia=datos.dia_venta
        venta.hora=datos.hora_venta
        venta.carrito_id = datos.carrito_id
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
    carrito = venta.carrito
    productos = []
    precio_total = 0.0

    if carrito:
        items = db.query(Carrito_Producto).filter_by(id_carrito=carrito.id).all()

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
        "id": venta.id,
        "fecha": venta.dia,
        "hora": venta.hora,
        "precio_total": precio_total,
        "carrito": {
            "id": carrito.id if carrito else None,
            "fecha_creacion": carrito.fecha_creacion if carrito else None,
            "estado": carrito.estado if carrito else None,
            "productos": productos,
            "total": precio_total
        } if carrito else None
    }
