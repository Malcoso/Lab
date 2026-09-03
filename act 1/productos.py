from models import Producto

def altaprod(producto, db):
    try:
        db.add(producto)
        db.commit()
        db.refresh(producto)
        print("Producto agregado.")
        return producto
    except Exception as e:
        db.rollback()
        raise e

def mostrarprod(producto):
    return {

        "id Producto": producto.id,
        "nombre ": producto.nombre,
        "precio": producto.precio

    }

def modifprod(producto,datos,db):
    
    try:
        producto.nombre=datos.nombre
        producto.precio=datos.precio
        db.commit()
        db.refresh(producto)
        print("Producto modificado")
        return producto
    except Exception as e:
        db.rollback()
        raise e

def borraprod(producto,db):
    try:
        db.delete(producto)
        db.commit()
        print("Producto eliminado")
        return producto
    except Exception as e:
        db.rollback()
        raise e

def productosgen(db):
    productos = db.query(Producto).all()
    return productos

def busquedaprod(id,db):
    producto = db.query(Producto).filter_by(id=id).first()
    if producto:
        return producto
    else:
        return None

