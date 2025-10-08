from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    username: str = Field(min_length=5)
    firstname: str
    lastname: str
    password: str


class UserResponse(BaseModel):
    username: str
    firstname: str
    lastname: str


class PasswordRequest(BaseModel):
    password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
