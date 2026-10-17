Proyecto API de gestion de productos, carritos y ventas

Este proyecto es una API REST desarrollada con FastAPI y SQLAlchemy para gestionar:
- productos
- carritos
- productos dentro de cada carrito
- ventas asociadas a carritos

Tecnologias utilizadas:
- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

Estructura del proyecto:
- main.py
- database.py
- models.py
- schema.py
- productos.py
- carrito.py
- carrito_producto.py
- ventas.py
- routers/
  - productos.py
  - carritos.py
  - carrito_productos.py
  - ventas.py
- requirements.txt

Requisitos del entorno virtual:
Las dependencias del proyecto se encuentran en el archivo requirements.txt.

Para configurar el entorno virtual e instalar las dependencias del proyecto, ejecutar:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

En Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Ejecucion de la aplicacion:
Una vez configurado el entorno virtual y las dependencias, la API puede levantarse con cualquiera de los siguientes comandos:

fastapi run

O bien:

uvicorn main:app --reload

Endpoints principales:

Productos:
- GET /productos/
- GET /productos/{id}
- POST /productos/
- PUT /productos/{id}
- DELETE /productos/{id}

Carritos:
- GET /carritos/
- GET /carritos/{id}
- POST /carritos/
- PUT /carritos/{id}
- DELETE /carritos/{id}

Productos dentro del carrito:
- GET /carrito_productos/{id}/productos
- POST /carrito_productos/{id}/productos

Ventas:
- GET /ventas/
- GET /ventas/{id}
- POST /ventas/
- PUT /ventas/{id}
- DELETE /ventas/{id}

Base de datos:
La aplicacion usa SQLite y crea la base de datos automaticamente al iniciar.

Observacion:
Este proyecto fue desarrollado como ejemplo de practica para aprender FastAPI, validacion con Pydantic y relaciones con SQLAlchemy.
