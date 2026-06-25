from fastapi import FastAPI
from .orders import router as orders_router
from src.api.couriers import router as courier_router
from .partners import router as partner_router

app = FastAPI()

app.include_router(courier_router)
app.include_router(orders_router)
app.include_router(partner_router)
