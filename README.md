[README.md](https://github.com/user-attachments/files/32479385/README.md)
# Proyecto API de Carritos, Productos y Ventas

Este proyecto es una API REST desarrollada con FastAPI y SQLAlchemy para gestionar:

- productos
- carritos
- productos dentro de cada carrito
- ventas asociadas a carritos

## Tecnologías

- Python
- FastAPI
- SQLAlchemy
- SQLite

## Estructura del proyecto

- `main.py`: punto de entrada de la aplicación
- `database.py`: configuración de la base de datos
- `models.py`: modelos ORM
- `schema.py`: schemas de validación y respuesta
- `productos.py`: lógica de productos
- `carrito.py`: lógica de carritos
- `carrito_producto.py`: lógica de relación carrito-producto
- `ventas.py`: lógica de ventas
- `routers/`: endpoints de la API
  - `productos.py`
  - `carritos.py`
  - `carrito_productos.py`
  - `ventas.py`
- `requirements.txt`: dependencias del proyecto

## Requisitos del entorno virtual

Las dependencias del proyecto están en el archivo `requirements.txt`.

Para instalar todo directamente, ejecutá:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecutar la API

Una vez instalado el entorno virtual y las dependencias, podés levantar la aplicación con:

```bash
fastapi run
```

O bien:

```bash
uvicorn main:app --reload
```

## Endpoints principales

### Productos
- GET `/productos/`
- GET `/productos/{id}`
- POST `/productos/`
- PUT `/productos/{id}`
- DELETE `/productos/{id}`

### Carritos
- GET `/carritos/`
- GET `/carritos/{id}`
- POST `/carritos/`
- PUT `/carritos/{id}`
- DELETE `/carritos/{id}`

### Productos en carrito
- GET `/carrito_productos/{id}/productos`
- POST `/carrito_productos/{id}/productos`

### Ventas
- GET `/ventas/`
- GET `/ventas/{id}`
- POST `/ventas/`
- PUT `/ventas/{id}`
- DELETE `/ventas/{id}`

## Base de datos

La aplicación usa SQLite y crea la base de datos automáticamente al iniciar, a partir de `database.py` y `models.py`.

## Observación

Este proyecto fue desarrollado como ejemplo de práctica para aprender FastAPI, validación con Pydantic y relaciones con SQLAlchemy.
