from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel

# CUSTOMER    
class CustomerBase(BaseModel):
    name: str
    description: str | None
    email: EmailStr
    age: int

class Customer(CustomerBase, SQLModel, table=True):
    id: int | None = None  # Optional field with default value of None

class CustomerCreate(CustomerBase):
    pass

# TRANSACTION
class Transaction(BaseModel):
    id: int
    amount: int
    description: str
    date: str | None = None  # Optional field with default value of None

# INVOICE
class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    # Con @property puedes acceder así:
    # total = factura.ammount_total  # Sin paréntesis ()

    # Sin @property tendrías que acceder así:
    # total = factura.ammount_total()  # Con paréntesis

    @property
    def ammount_total(self):
        return sum(transaction.amount for transaction in self.transactions)
        
        # Explicación:
        # # ❌ Incorrecto:
        # for persona.nombre in lista_personas:
        #     print(persona.nombre)

        # # ✅ Correcto:
        # for persona in lista_personas:
        #     print(persona.nombre)