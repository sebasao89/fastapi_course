from fastapi import APIRouter

from models import Transaction

router = APIRouter()  # Crea un enrutador para manejar las rutas de la aplicación



@router.post("/transaction", tags=["transactions"])
async def create_transaction(transaction_data: Transaction):
    return transaction_data