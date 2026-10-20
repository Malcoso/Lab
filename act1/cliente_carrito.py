from models import Clientes_Has_Carritos

from cliente import busquedacliente,mostrarcliente
from carrito import busquedacarrito,mostrarcarrito

def getidcarrito_cliente(cliente_has_carrito):
    return cliente_has_carrito.carrito_id

def getidcliente(cliente_has_carrito):
    return cliente_has_carrito.cliente_id

def getidcarrito(cliente_has_carrito):
    return cliente_has_carrito.carrito_id

def setidcliente(cliente_has_carrito, cliente_id):
    cliente_has_carrito.cliente_id = cliente_id
    return cliente_has_carrito

def setidcarrito(cliente_has_carrito, carrito_id):
    cliente_has_carrito.carrito_id = carrito_id
    return cliente_has_carrito

def altacliente_carrito(cliente_has_carrito, db):
    try:
        db.add(cliente_has_carrito)
        db.commit()
        db.refresh(cliente_has_carrito)
        return cliente_has_carrito
    except Exception as e:
        db.rollback()
        raise e

def modifcliente_carrito(cliente_has_carrito, datos, db):
    try:
        setidcliente(cliente_has_carrito, datos.cliente_id)
        setidcarrito(cliente_has_carrito, datos.carrito_id)
        db.commit()
        db.refresh(cliente_has_carrito)
        return cliente_has_carrito
    except Exception as e:
        db.rollback()
        raise e

def eliminarcliente_carrito(cliente_has_carrito, db):
    try:
        db.delete(cliente_has_carrito)
        db.commit()
        return cliente_has_carrito
    except Exception as e:
        db.rollback()
        raise e


def clientes_has_carritosgen(db):
    clientes_has_carritos = db.query(Clientes_Has_Carritos).all()
    if clientes_has_carritos:
        return [mostrarcliente_carrito(c,db) for c in clientes_has_carritos]
    else:
        return None

def mostrarcliente_carrito(cliente_has_carrito,db):
    cliente = busquedacliente(cliente_has_carrito.cliente_id, db)
    carrito = busquedacarrito(cliente_has_carrito.carrito_id, db)
    return {
        "id": getidcarrito_cliente(cliente_has_carrito),
        "cliente": mostrarcliente(cliente, db) if cliente else None,
        "carrito": mostrarcarrito(carrito, db) if carrito else None
    }

