import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select


myapp = FastAPI(lifespan = create_all_tables)  # Crea una instancia de FastAPI y registra la función create_all_tables como un evento de inicio y cierre de la aplicación

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

current_id: int = 0

db_customers: list[Customer] = []


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

@myapp.post("/customer", response_model=Customer)   #response_model es para que devuelva el modelo de Customer
async def create_customer(customer_data: CustomerCreate, session: SessionDep):   #Este modelo es el que se usa para crear un cliente
    customer = Customer.model_validate(customer_data.model_dump())  #model_validate es para validar el modelo que ingresan, y debemos pasar un diccionario
    session.add(customer)  #session es la sesión de la base de datos, y add es para agregar el cliente a la base de datos
    session.commit()  #session.commit() es para guardar los cambios en la base de datos
    session.refresh(customer)  #session.refresh(customer) es para refrescar el cliente y obtener el id que se le asignó en la base de datos
    #customer.id = len(db_customers)
    #db_customers.append(customer)
    #return customer_data           #customer_data es el que se pasa como parámetro, y 
    return customer     #customer es el que se devuelve como respuesta

@myapp.get("/customers", response_model=list[Customer])  #response_model es para que devuelva una lista de Customer
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()  #session.exec(select(Customer)).all() es para obtener todos los clientes de la base de datos
    #return db_customers

@myapp.get("/customer/{customer_id}", response_model=Customer)  #response_model es para que devuelva un Customer
async def get_customer(customer_id: int):
    for customer in db_customers:
        if customer.id == customer_id:
            return customer
    return {"message": "Customer not found"}

@myapp.post("/transaction")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@myapp.post("/invoice")
async def create_invoice(invoice_data: Invoice):
    return invoice_data