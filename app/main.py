import zoneinfo
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from db import create_all_tables
from .routers import customers, transactions, invoices, plans # Importa el enrutador de clientes, transacciones e invoices


@asynccontextmanager
async def lifespan(myapp: FastAPI) -> AsyncGenerator[None, None]:
    """Gestiona el ciclo de vida de la aplicación"""
    try:
        await create_all_tables()
        yield
    finally:
        # Aquí puedes agregar código de limpieza si es necesario
        pass

myapp = FastAPI(lifespan=lifespan)  # Crea una instancia de FastAPI y registra la función lifespan como un evento de inicio y cierre de la aplicación
myapp.include_router(customers.router)  # Incluye el enrutador de clientes en la aplicación FastAPI
myapp.include_router(transactions.router)  # Incluye el enrutador de transacciones en la aplicación FastAPI
myapp.include_router(invoices.router)  # Incluye el enrutador de invoices en la aplicación FastAPI
myapp.include_router(plans.router)  # Incluye el enrutador de invoices en la aplicación FastAPI

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
async def get_time_by_country(variable_iso_code: str):
    iso = variable_iso_code.upper()
    timezone_str = country_timezones.get(iso)
    if timezone_str is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró la zona horaria para el país {iso}"
        )
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"Time": datetime.now(tz)}


