from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import SessionDep
from models import Customer, Transaction, TransactionCreate

router = APIRouter()  # Crea un enrutador para manejar las rutas de la aplicación



@router.post("/transaction", status_code=status.HTTP_201_CREATED, tags=["transactions"])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict["customer_id"])
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {transaction_data_dict['customer_id']} not found",
        )
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db


@router.get("/transactions", status_code=status.HTTP_200_OK, tags=["transactions"])
async def list_transactions(session: SessionDep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions