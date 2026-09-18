from models import Carrito,Carrito_Producto
from productos import mostrarprod,busquedaprod

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
        "ID Carrito ": carrito_producto.id_carrito,
        "Carrito ": mostrarcarrito(carrito_producto.carrito),
        "ID Producto ": carrito_producto.id_producto,
        "Producto ": mostrarprod(carrito_producto.producto),
        "Cantidad producto": carrito_producto.cantidad
    }


def carrito_productogen(db):
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

def agregar_producto_carrito(db,id_carrito,id_producto,cantidad):
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
