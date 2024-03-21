from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class Users(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class Userdb(Users):
    password: str


users_db = {
    "erikdev": {
        "username": "erikdev",
        "full_name": "Erik Caceres",
        "email": "erik@gmail.com",
        "disabled": False,
        "password": "$2a$12$p.BFGib3c3egZMYXfb8pmuDENJYfZfE8lTCYHjUH.AfFylXvI.wMq",
    },
    "erikdev2": {
        "username": "erikdev2",
        "full_name": "Erik Caceres2",
        "email": "erik2@gmail.com",
        "disabled": True,
        "password": "$2a$12$rxFGYmi0tw.F2la.edgNjeRGSOtWmeWMDTu88iGdPz9ZW3yaijDdO",
    },
}


def search_user_db(username: str):
    if username in users_db:
        return Userdb(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return Users(**users_db[username])


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and generates an access token.

    Args:
        form (OAuth2PasswordRequestForm): The form containing the user's login credentials.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no encontrado"
        )

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta"
        )

    access_token = {
        "sub": user.username,
        "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer",
    }


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Credenciales no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: Users = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo"
        )
    return user


@router.get("/users/me")
async def me(user: Users = Depends(current_user)):
    return user
