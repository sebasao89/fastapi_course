from pydantic import BaseModel, EmailStr
# SQLModel es una biblioteca que combina SQLAlchemy y Pydantic para facilitar la creación de modelos de datos y la interacción con bases de datos en aplicaciones FastAPI.
#Field conecta un campo de un modelo a una columna de una tabla en la base de datos
from sqlmodel import SQLModel, Field

# CUSTOMER    
class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)  # Optional field with default value of None
    email: EmailStr = Field(default=None)  # EmailStr is a Pydantic type for email validation
    age: int = Field(default=None) 

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Optional field with default value of None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
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