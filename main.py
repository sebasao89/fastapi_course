import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from models import Customer, CustomerCreate, Transaction, Invoice


myapp = FastAPI()

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

@myapp.post("/customer", response_model=Customer) #response_model es para que devuelva el modelo de Customer
async def create_customer(customer_data: CustomerCreate): #Este modelo es el que se usa para crear un cliente
    customer = Customer.model_validate(customer_data.model_dump) #model_validate es para validar el modelo que se ingresan, y debemos pasar un diccionario
    customer.id = current_id + 1
    #return customer_data           #customer_data es el que se pasa como parámetro, y 
    return customer #customer es el que se devuelve como respuesta

@myapp.post("/transaction")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@myapp.post("/invoice")
async def create_invoice(invoice_data: Invoice):
    return invoice_data