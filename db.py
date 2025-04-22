# La importación 'Annotated' de typing permite agregar metadatos a las anotaciones de tipo,
# lo que es útil para proporcionar información adicional sobre los tipos en tiempo de ejecución
# sin afectar la verificación de tipos estática. En FastAPI, se usa comúnmente para inyección
# de dependencias y validación de parámetros.
from typing import Annotated

from fastapi import Depends, FastAPI                         # Importa la clase Depends de FastAPI para manejar dependencias

from sqlmodel import SQLModel, Session, create_engine         # Crea una sesión para conectar a la base de datos


# MOTOR DE BASE DE DATOS SQLITE

sqlite_name = "db.sqlite3"                          # Nombre de la base de datos SQLite
sqlite_url = f"sqlite:///{sqlite_name}"             # URL de conexión a la base de datos SQLite

engine = create_engine(sqlite_url)                  # Crea un motor de base de datos SQLite


# CREA LA BD Y LAS TABLAS SI NO EXISTEN
def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)           # Crea todas las tablas definidas en los modelos SQLModel
    yield                                          # La función yield se utiliza para crear un generador, que permite pausar la ejecución y devolver un valor temporalmente

# OBTENER UNA SESIÓN DE BASE DE DATOS
def get_session():
    with Session(engine) as session:
        yield session
        # yield es una palabra clave que se utiliza en Python para crear generadores.

# Registra la sesion como una dependencia para todos nuestros endpoints
SessionDep = Annotated[
    Session,                                        # Tipo de la dependencia
    Depends(get_session),                           # Dependencia que se inyectará
]  # SessionDep es una anotación que indica que se espera una sesión de base de datos como dependencia  