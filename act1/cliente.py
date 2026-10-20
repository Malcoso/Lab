from models import Clientes, Clientes_Has_Carritos


def getidcliente(cliente):
    return cliente.id

def getnombrecliente(cliente):
    return cliente.nombre

def getemailcliente(cliente):
    return cliente.email

def gettelefonocliente(cliente):
    return cliente.telefono

def setnombrecliente(cliente,nombre):
    cliente.nombre = nombre

def setemailcliente(cliente,email):
    cliente.email = email

def settelefonocliente(cliente,telefono):
    cliente.telefono = telefono

def altacliente(cliente,db):
    try:
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    except Exception as e:
        db.rollback()
        raise e

def modifcliente(cliente,datos,db):
    try:
        setnombrecliente(cliente,datos.nombre)
        setemailcliente(cliente,datos.email)
        settelefonocliente(cliente,datos.telefono)
        db.commit()
        db.refresh(cliente)
        return cliente
    except Exception as e:
        db.rollback()
        raise e

def clientesgen(db):
    clientes = db.query(Clientes).all()
    if clientes:
        return [mostrarcliente(c,db) for c in clientes]
    else:
        return None

def mostrarcliente(cliente,db):
    carritos_asociados = busquedaclientes_has_carritos(cliente, db)
    carritos_info = []
    for asociacion in carritos_asociados:
        carrito = asociacion.carrito
        if carrito:
            carritos_info.append({
                "id": carrito.id,
                "fecha_creacion": carrito.fecha_creacion,
                "estado": carrito.estado
            })
    return {
        "id": getidcliente(cliente),
        "nombre": getnombrecliente(cliente),
        "email": getemailcliente(cliente),
        "telefono": gettelefonocliente(cliente),
        "carritos_asociados": carritos_info
    }

def eliminarcliente(cliente,db):
    try:
        db.delete(cliente)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e

def busquedaclientes_has_carritos(cliente,db):
    return db.query(Clientes_Has_Carritos).filter(Clientes_Has_Carritos.cliente_id == cliente.id).all()

def busquedacliente(id,db):
    cliente = db.query(Clientes).filter(Clientes.id == id).first()
    return mostrarcliente(cliente, db) if cliente else None