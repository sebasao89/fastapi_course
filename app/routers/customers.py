from fastapi import APIRouter,HTTPException, status
from sqlmodel import select

from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDep

router = APIRouter()  # Crea un enrutador para manejar las rutas de la aplicación

db_customers: list[Customer] = []


@router.post("/customer", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])             #response_model es para que devuelva el modelo de Customer
async def create_customer(customer_data: CustomerCreate, session: SessionDep):   #Este modelo es el que se usa para crear un cliente
    customer = Customer.model_validate(customer_data.model_dump())               #model_validate es para validar el modelo que ingresan, y debemos pasar un diccionario
    session.add(customer)                                                        #session es la sesión de la base de datos, y add es para agregar el cliente a la base de datos
    session.commit()                                                             #session.commit() es para guardar los cambios en la base de datos
    session.refresh(customer)                                                    #session.refresh(customer) es para refrescar el cliente y obtener el id que se le asignó en la base de datos
    #customer.id = len(db_customers)
    #db_customers.append(customer)
    #return customer_data           #customer_data es el que se pasa como parámetro, y 
    return customer 
                                                             #customer es el que se devuelve como respuesta

@router.get("/customer/{customer_id}", response_model=Customer, tags=["customers"])                   #response_model es para que devuelva un Customer
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)                             #session.get(Customer, customer_id) es para obtener el cliente de la base de datos, los parametros son el modelo y el id con el que se busca
    if not customer_db:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Customer not found")   #HTTPException es para lanzar una excepción si no se encuentra el cliente
    return customer_db


@router.patch("/customer/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK, tags=["customers"])  #response_model es para que devuelva un Customer              
async def update_customer(customer_id: int, customer_data: CustomerUpdate ,session: SessionDep):
    customer_db = session.get(Customer, customer_id)                                
    if not customer_db:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Customer not found")   
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)  #sqlmodel_update es para actualizar el cliente en la base de datos
    session.add(customer_db)  #session.add(customer_db) es para agregar el cliente a la base de datos
    session.commit()
    session.refresh(customer_db)
    return customer_db


@router.get("/customers", response_model=list[Customer], tags=["customers"])  #response_model es para que devuelva una lista de Customer
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()  #session.exec(select(Customer)).all() es para obtener todos los clientes de la base de datos
    #return db_customers


@router.get("/customer1/{customer_id}", response_model=Customer, tags=["customers"])  #response_model es para que devuelva un Customer
async def get_customer(customer_id: int):
    for customer in db_customers:
        if customer.id == customer_id:
            return customer
    return {"message": "Customer not found"}


@router.delete("/customer/{customer_id}", tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)  #session.get(Customer, customer_id) es para obtener el cliente de la base de datos
    if not customer_db:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Customer not found")  #HTTPException es para lanzar una excepción si no se encuentra el cliente
    session.delete(customer_db)
    session.commit()
    return {"detail": "Customer deleted"}