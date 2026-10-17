from models import Producto

def getprecioproducto(producto):
    return producto.precio

def getnombreproducto(producto):
    return producto.nombre

def getidproducto(producto):
    return producto.id

def setnombreproducto(producto,nombre):
    producto.nombre=nombre
    return producto

def setprecioproducto(producto,precio):
    producto.precio=precio
    return producto

def altaprod(producto, db):             #Alta producto
    try:
        db.add(producto)
        db.commit()
        db.refresh(producto)
        print("Producto agregado.")
        return producto
    except Exception as e:
        db.rollback()
        raise e

def modifprod(producto,datos,db):       #Modificacion producto
    try:
        setnombreproducto(producto,datos.nombre)
        setprecioproducto(producto,datos.precio)
        db.commit()
        db.refresh(producto)
        print("Producto modificado")
        return producto
    except Exception as e:
        db.rollback()
        raise e

def borraprod(producto,db):             #Borra el producto
    try:
        db.delete(producto)
        db.commit()
        print("Producto eliminado")
        return producto
    except Exception as e:
        db.rollback()
        raise e

def productosgen(db):                       #Muestra todos los productos
    productos = db.query(Producto).all()
    return productos

def busquedaprod(id,db):                                 #Busca el producto elegido
    producto = db.query(Producto).filter_by(id=id).first()
    if producto:
        return producto
    else:
        return None

def busquedaprodnombre(nombre,db):
    producto = db.query(Producto).filter(Producto.nombre == nombre).first()
    if producto:
        return producto
    else:
        return None
