from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


# Entidad user

# Pydancitc: es una libreria que permite validar datos JSON y convertirlos en objetos Python.
# BaseModel: es una clase de Pydantic que se utiliza para definir
# modelos de datos que se utilizan para validar datos JSON y convertirlos en objetos Python.
# como funciona BaseModel: https://pydantic-docs.helpmanual.io/usage/models/


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


user_list = [
    User(id=1, name="Erik", surname="Caceres", url="https://erikdev.com", age=25),
    User(id=2, name="Brais", surname="Moure", url="https://moure.dev", age=35),
    User(id=3, name="Juan", surname="Perez", url="https://juandev.com", age=33),
]

# APIRouter: es una clase de FastAPI que se utiliza para definir rutas y operaciones de API.
# tags: es una palabra clave que se utiliza para definir las etiquetas de la ruta.
# responses: es una palabra clave que se utiliza para definir las respuestas de la ruta.
router = APIRouter(tags=["users"], responses={404: {"description": "Not found"}})


@router.get("/usersjson/")
async def users_json():
    return [
        {"name": "Erik", "surname": "Caceres", "url": "https://erikdev.com", "age": 25},
        {"name": "Brais", "surname": "Moure", "url": "https://moure.dev", "age": 35},
        {"name": "Juan", "surname": "Perez", "url": "https://juandev.com", "age": 33},
    ]


@router.get("/users/")
async def users():
    """
    Retrieve a list of users.

    Returns:
        List[User]: A list of user objects.
    """
    return user_list


# Path: es una variable que se puede pasar en la URL
# ejemplo: http://localhost:8000/user/1
@router.get("/user/{id}")
async def user(id: int):
    """
    Retrieve user information based on the provided ID.

    Parameters:
    - id (int): The ID of the user to retrieve.

    Returns:
    - User: The user object containing the information.

    """
    return search_user(id)


# que es query: es una variable que se puede pasar en la URL
# ejemplo: http://localhost:8000/userquery/?id=1
@router.get("/user/")
async def user(id: int):
    return search_user(id)


# response_model: es una palabra clave que se utiliza para definir el modelo de datos
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    """
    Create a new user.

    Args:
        user (User): The user object containing user details.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If the user already exists.
    """
    if type(search_user(user.id)) == User:
        # raise: es una palabra clave que se utiliza para lanzar una excepción.
        raise HTTPException(status_code=404, detail="User already exists")
    else:
        user_list.append(user)
        return user


@router.put("/user/")
async def user(user: User):
    """
    Update a user in the user_list based on the provided user object.

    Args:
        user (User): The user object containing the updated information.

    Returns:
        dict: The updated user object if found, or a message indicating that the user was not found.
    """
    found = False

    for index, save_user in enumerate(user_list):
        if save_user.id == user.id:
            user_list[index] = user
            found = True

    # significado: si no se encuentra el usuario
    # se retorna un mensaje de error
    if not found:
        return {"message": "User not found"}
    else:
        return user


@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, save_user in enumerate(user_list):
        if save_user.id == id:
            del user_list[index]
            found = True

    # significado: si no se encuentra el usuario
    # se retorna un mensaje de error
    if not found:
        return {"message": "User not found"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        return {"message": "User not found"}


# iniciar
# uvicorn users:app --reload
