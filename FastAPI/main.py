# API: es la interfaz de programación de aplicaciones que permite
# a los desarrolladores de software interactuar con otras aplicaciones o servicios.

# FastAPI: es un marco moderno (framework) y rápido para crear API con Python 3.7+
# con una sintaxis fácil de usar y una gran cantidad de funciones y herramientas.

from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return "Hello World"


@app.get("/url")
async def url():
    return {"url": "https://google.com"}


# iniciar server: uvicorn main:app --reload

# async: es una palabra clave que se utiliza para definir funciones asincrónicas.
# funciones asyncronas: son funciones que pueden esperar
# a que se realicen operaciones y no bloquean el hilo de ejecución.
# funciones sincronas: son funciones que no pueden
# esperar a que se realicen operaciones y bloquean el hilo de ejecución.
