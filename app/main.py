import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from models import Transaction, Invoice
from db import create_all_tables
from .routers import customers # Importa el enrutador de clientes



myapp = FastAPI(lifespan = create_all_tables)  # Crea una instancia de FastAPI y registra la función create_all_tables como un evento de inicio y cierre de la aplicación
myapp.include_router(customers.router)  # Incluye el enrutador de clientes en la aplicación FastAPI

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

current_id: int = 0


# ENDPOINTS

@myapp.get("/")
def read_root():
    return {"message": "Hello, FastAPI! by sebasao"}

@myapp.get("/time")
async def time():
    return {"Time": datetime.now()}

    # endpoint with a variable
@myapp.get("/time2/{variable_iso_code}")
async def time(variable_iso_code: str):
    iso = variable_iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"Time": datetime.now(tz)}







@myapp.post("/transaction")
async def create_transaction(transaction_data: Transaction):
    return transaction_data



@myapp.post("/invoice")
async def create_invoice(invoice_data: Invoice):
    return invoice_data