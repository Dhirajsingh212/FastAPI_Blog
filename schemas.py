from pydantic import BaseModel, Field


# USER MODELS
class UserRequest(BaseModel):
    username: str = Field(min_length=5)
    firstname: str
    lastname: str
    password: str


class UserResponse(BaseModel):
    username: str
    firstname: str
    lastname: str


# SECURITY MODELS
class PasswordRequest(BaseModel):
    password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# BLOG MODELS
class BlogRequest(BaseModel):
    title: str
    description: str
