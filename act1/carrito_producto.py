from models import Carrito_Producto

def altacarrito_producto(idcarrito,carrito_producto,db):
    try:
        item = db.query(Carrito_Producto).filter_by(
        id_carrito=idcarrito,
        id_producto=carrito_producto.id_producto
    ).first()
        if item:
            item.cantidad +=carrito_producto.cantidad
        else:
            item = Carrito_Producto(
                id_carrito=idcarrito,
                id_producto=carrito_producto.id_producto,
                cantidad=carrito_producto.cantidad
                )
            db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except Exception as e:
        db.rollback()
        raise e

def mostrarcarrito_producto(item):
    producto = item.producto
    return {
        "id": item.id,
        "id_producto": item.id_producto,
        "cantidad": item.cantidad,
        "subtotal": (producto.precio * item.cantidad) if producto else 0,
        "producto": {
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio
        } if producto else None
    }

def carrito_prodgen(db):
    carrito_prod=db.query(Carrito_Producto).all()
    if carrito_prod:
        return carrito_prod
    else:
        return None

def busquedacarrito_prod(id,db):
    carrito_prod=db.query(Carrito_Producto).filter_by(id=id).first()
    if carrito_prod:
        return carrito_prod
    else:
        return None

def busquedacarritos_prod(id_carrito,db):
    carrito_producto=db.query(Carrito_Producto).filter_by(id_carrito=id_carrito).all()
    if carrito_producto is None:
        return  None
    return carrito_producto

def busq_prod_carrito(db,id_carrito,id_producto):
    carrito_producto = db.query(Carrito_Producto).filter_by(id_carrito=id_carrito,id_producto=id_producto).first()
    if carrito_producto:
        return carrito_producto
    else:
        return None

def borrar_prod_carrito(db,prod_carrito):
    try:
        db.delete(prod_carrito)
        db.commit()
        return prod_carrito
    except Exception as e:
        raise e

def buquedaprod_carrito_producto(id,db):
    db.query(Carrito_Producto).filter(Carrito_Producto.id_producto==id).first()
