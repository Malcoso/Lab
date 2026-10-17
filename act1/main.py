from fastapi import FastAPI

from routers.productos import router as productos_router
from routers.ventas import router as ventas_router
from routers.carritos import router as carritos_router
from routers.carrito_productos import router as carrito_productos_router

app = FastAPI()

app.include_router(productos_router)
app.include_router(carritos_router)
app.include_router(carrito_productos_router)
app.include_router(ventas_router)

    
        

