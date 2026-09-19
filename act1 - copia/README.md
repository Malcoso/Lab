# API de productos y ventas

API REST desarrollada con Python, FastAPI, SQLAlchemy y SQLite. Permite
administrar productos y registrar ventas asociadas a ellos.

## Requisitos

- Python 3.10 o superior
- `pip`

## Instalacion

1. Crea y activa un entorno virtual:

	 ```powershell
	 python -m venv .venv
	 .venv\Scripts\Activate.ps1
	 ```

	 En Linux o macOS, activa el entorno con:

	 ```bash
	 source .venv/bin/activate
	 ```

2. Instala las dependencias:

	 ```bash
	 pip install fastapi[standard] sqlalchemy
	 ```

## Ejecucion

Desde la carpeta del proyecto, ejecuta:

```bash
uvicorn main:app --reload
```

La API estara disponible en:

- http://127.0.0.1:8000
- Documentacion interactiva Swagger: http://127.0.0.1:8000/docs
- Documentacion alternativa ReDoc: http://127.0.0.1:8000/redoc

Al iniciar la aplicacion se crea el archivo `mydb.db`, que contiene la base
de datos SQLite.

## Endpoints

### Productos

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `POST` | `/productos` | Crear un producto |
| `GET` | `/productos/` | Listar todos los productos |
| `GET` | `/productos/{id}` | Consultar un producto |
| `PUT` | `/productos/{id}` | Modificar un producto |
| `DELETE` | `/productos/{id}` | Eliminar un producto |

Ejemplo para crear un producto:

```json
{
	"nombre": "Teclado",
	"precio": 25.5
}
```

### Ventas

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `POST` | `/ventas` | Registrar una venta |
| `GET` | `/ventas/` | Listar todas las ventas |
| `GET` | `/ventas/{id}` | Consultar una venta |
| `PUT` | `/ventas/{id}` | Modificar una venta |
| `DELETE` | `/ventas/{id}` | Eliminar una venta |

Ejemplo para registrar una venta del producto con ID `1`:

```json
{
	"producto_id": 1,
	"cantidad": 2
}
```

El campo `precio_total` se calcula automaticamente usando el precio del
producto y la cantidad vendida.

## Estructura del proyecto

```text
.
├── database.py   # Configuracion de SQLite y sesiones SQLAlchemy
├── main.py       # Aplicacion FastAPI y endpoints
├── models.py     # Modelos Producto y Venta
├── productos.py  # Operaciones de productos
├── ventas.py     # Operaciones de ventas
└── README.md     # Documentacion del proyecto
```

## Validaciones

- No se puede crear una venta para un producto inexistente.
- La cantidad de una venta debe ser mayor que cero.
- Las consultas, modificaciones y eliminaciones de IDs inexistentes devuelven
	un error `404`.