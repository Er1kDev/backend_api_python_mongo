from pydantic import BaseModel, Field


class User(BaseModel):
    id: str | None = Field(None)
    username: str
    email: str
