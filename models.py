from pydantic import BaseModel, EmailStr
# SQLModel es una biblioteca que combina SQLAlchemy y Pydantic para facilitar la creación de modelos de datos y la interacción con bases de datos en aplicaciones FastAPI.
#Field conecta un campo de un modelo a una columna de una tabla en la base de datos
from sqlmodel import Relationship, SQLModel, Field


# RELATIONSHIP
class CustomerPlan(SQLModel, table=True):
    plan_id: int = Field(foreign_key="plan.id", primary_key=True)  # Foreign key to the Plan table
    customer_id: int = Field(foreign_key="customer.id", primary_key=True)  # Foreign key to the Customer table
    plan_id: int = Field(foreign_key="plan.id")  # Foreign key to the Plan table


# PLAN
class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Optional field with default value of None
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str | None = Field(default=None)  # Optional field with default value of None
    customers: list["Customer"] = Relationship(back_populates="plans", link_model=CustomerPlan)  # Relationship to the Customer table


# CUSTOMER    
class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)  # Optional field with default value of None
    email: EmailStr = Field(default=None)  # EmailStr is a Pydantic type for email validation
    age: int = Field(default=None) 

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Optional field with default value of None
    transactions: list["Transaction"] = Relationship(back_populates="customer")  # Relationship to the Transaction table
    plans: list["Plan"] = Relationship(back_populates="customers", link_model=CustomerPlan)  # Relationship to the Plan table

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass


# TRANSACTION
class TransactionBase(SQLModel):
    amount: int = Field(default=None)
    description: str = Field(default=None)  # Optional field with default value of None

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")  # Foreign key to the Customer table
    customer: Customer = Relationship(back_populates="transactions")  # Relationship to the Customer table

class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")


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