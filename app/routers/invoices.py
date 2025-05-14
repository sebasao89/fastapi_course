from fastapi import APIRouter

from models import Invoice

router = APIRouter()  # Crea un enrutador para manejar las rutas de la aplicación



@router.post("/invoice", tags=["invoices"])
async def create_invoice(invoice_data: Invoice):
    return invoice_data